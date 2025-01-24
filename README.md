# Introduction
Script to bulk-update Gmail signatures for Google Workspace.

# Setup
## 1. Create Google Service Account credentials
A good example to get service account credentials from Google Cloud Console.
1. https://support.templafy.com/hc/en-us/articles/4707610312221-How-to-set-up-the-Service-Account-required-for-enabling-Gmail-signature-integration-in-Templafy-
2. Save the credentials as `token.json`

## 2. Signature template and Google users
1. Copy `template.example.html` to `template.html` and modify the file. 
2. Copy `users.example.json` to `users.json` and modify the file.

## 3. Build and run Containers
```bash
# Build the Docker image
docker build -t gmail-signature .

# Run the script inside a container
cat script.py | docker run -i --rm -v `pwd`:/data -w /data gmail-signature
```

## 3. Alternative Build and run UV
```bash
uv run script.py
```

### 4. Run Google script
1. Go to `script.google.com`
2. Paste content of workspace2json.gs inside editor
3. Adjust values to match your domain
4. Run script, and give permission of admin user
5. Find json in admin drive.
6. Use json to run script