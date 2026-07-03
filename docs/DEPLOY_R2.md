# Deploy incrementale su Cloudflare R2

Perché: GitHub Pages fa un **full-snapshot sync** di tutti i ~31k file a ogni
deploy (nessun incrementale) e a conteggi alti fallisce a intermittenza
(`syncing_files` → *"Deployment failed, try again later"*). Con **R2 + `rclone
sync`** l'upload notturno è il **solo delta** (gli enti che cambiano
classificazione + i loro vicini + gli hub impattati + i sitemap: centinaia di
file, non 31k). Elimina la fragilità, scala a qualunque numero di file, R2 non
ha costi di egress.

Rischio della migrazione: **basso**. `mxmap.it` **non ha MX** (nessuna email da
preservare); gli unici record sono l'apex (→ GitHub Pages), il CNAME
`osservatorio` → `fpietrosanti.github.io`, e un TXT `google-site-verification`.
Ogni passo è **reversibile** finché non si collega il custom domain a R2.

## Cosa fa Claude (già pronto)
- [`.github/workflows/deploy-r2.yml`](../.github/workflows/deploy-r2.yml): genera le
  pagine #15 e fa `rclone sync . → r2:<bucket>` con `--checksum` (confronto per
  hash, non per mtime — altrimenti il checkout ri-caricherebbe tutto). È
  `workflow_dispatch` e **inerte** finché non ci sono i secret.

## Cosa devi fare tu (una volta)

### 1. Cloudflare: aggiungi la zona
1. Crea/usa un account Cloudflare (piano **Free** basta).
2. **Add a site** → `mxmap.it` → Free. Cloudflare importa i record esistenti:
   **verifica** che ci siano l'apex `mxmap.it` (4 A record `185.199.108-111.153`),
   il CNAME `osservatorio` → `fpietrosanti.github.io`, e il TXT
   `google-site-verification`. (Nessun MX: giusto così.)

### 2. Registrar: cambia i nameserver
Cloudflare ti dà 2 nameserver (es. `xxx.ns.cloudflare.com`). Nel pannello del
**registrar** di mxmap.it (oggi usa `*.topdns.com`), sostituisci i nameserver con
quelli di Cloudflare. Propagazione: minuti–ore. **Il sito resta su GitHub Pages**
(i record sono stati importati) — nessun downtime.

### 3. R2: bucket + custom domain
1. Cloudflare → **R2** → *Create bucket* → nome es. `mxmap-it-site`.
2. **NON** collegare ancora il custom domain: prima lo riempiamo (passo 6).

### 4. R2: API token
Cloudflare → R2 → **Manage R2 API Tokens** → *Create API token* → permesso
**Object Read & Write**, scoped al bucket. Annota: **Access Key ID**, **Secret
Access Key**, e il tuo **Account ID** (in alto a destra / nella endpoint URL).

### 5. GitHub: secret
Repo `mxmap-it/mxmap.it` → *Settings → Secrets and variables → Actions* → aggiungi:
| Secret | Valore |
|---|---|
| `R2_ACCOUNT_ID` | il tuo Cloudflare Account ID |
| `R2_ACCESS_KEY_ID` | Access Key ID del token R2 |
| `R2_SECRET_ACCESS_KEY` | Secret Access Key del token R2 |
| `R2_BUCKET` | `mxmap-it-site` (il nome del bucket) |

### 6. Primo sync + cutover (con Claude)
1. Dimmi che i secret sono pronti → lancio `deploy-r2.yml` (workflow_dispatch):
   riempie il bucket col sito completo (verifica del `rclone sync`).
2. Verifichiamo il contenuto del bucket.
3. **Cutover** (reversibile): R2 → bucket → *Settings → Custom Domains* →
   *Connect Domain* → `mxmap.it`. Cloudflare crea il record + il certificato e
   inizia a servire da R2. (Per tornare indietro: disconnetti → riappaiono gli A
   record → GitHub Pages.)
4. Verifichiamo `https://mxmap.it/` + `/ente/...` + `/sitemap.xml`.
5. Abilito il trigger `push:` in `deploy-r2.yml` e faccio chiamare il deploy R2
   dalla nightly; ritiriamo i deploy GitHub Pages.

## Note
- **Cache-Control**: Cloudflare mette la sua cache CDN davanti a R2; per il
  `.html` conviene una regola di cache breve/`no-cache` così gli aggiornamenti
  notturni si vedono subito (si può fare con una Cache Rule su `*.html` o
  impostando l'header in fase di sync). Da tarare al passo 6.
- **`404.html`**: aggiungibile in root per una pagina 404 gradevole servita da R2.
- Cloudflare *Pages* NON va bene (limite 20.000 file/deploy < 31k): serve R2.
