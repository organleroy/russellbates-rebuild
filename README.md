# Russell Bates Portfolio (Eleventy rebuild)

## 1) Install
```bash
npm install
```

## 2) Extract content + thumbnails from your Simply Static export
First unzip your Simply Static export somewhere, then run:

```bash
python3 -m pip install beautifulsoup4
npm run extract -- /path/to/simply-static-export
```

This will:
- generate `src/content/projects.json`
- copy `/wp-content/uploads/` into `src/assets/uploads/`

## 3) Run locally
```bash
npm run dev
```
Open http://localhost:8080

## 4) Build
```bash
npm run build
```

## 5) Deploy to GitHub Pages
Commit + push the generated project source (NOT the `_site` folder) and let Pages build from branch.
