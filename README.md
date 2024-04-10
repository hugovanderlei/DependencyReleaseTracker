# SPM Release Tracker
![Captura de Tela 2024-04-09 às 21 21 52](https://github.com/hugovanderlei/SPM-Release-Tracker/assets/184836/7f31905f-2674-45ab-bf39-ab14f54d43bd)

## Overview
SPM Release Tracker is a tool designed to list release notes of Swift Package Manager (SPM) dependencies in a Swift project. It sorts these notes by the most recent and indicates which packages are updated or outdated, helping developers stay informed about their project's package changes.

## Features
- **Default Mode**: By default, it lists packages whose versions differ from those in the project's `Package.resolved`.
- **`--all` Option**: When used, it shows release notes for all versions of the dependencies, not just the ones that have been updated.

## Installation

To install Python via Homebrew on macOS, run:
```bash
brew install python
```
This installs the latest Python version. Verify the installation with `python3 --version`.

Install via pip:
```bash
pip install spm-release-tracker
```
## Usage
Navigate to the root directory of your Swift project and execute: 
```bash
spm-updates
```
Ensure you are in the directory containing the `.xcworkspace` to correctly list the release notes of Swift Package Manager (SPM) dependencies.

To see release notes for all versions, use the --all option:
```bash
spm-updates --all
```

## GitHub Token
For private repositories or to increase API rate limit, a GitHub token is required:

1. Go to [GitHub settings](https://github.com/settings/tokens).
2. Navigate to "Developer settings" > "Personal access tokens".
3. Click "Generate new token", give it a name, set an expiration, and select the `repo` scope.
4. Click "Generate token" and copy the generated token.
5. Save it securely and set it as an environment variable:

To set the GitHub token as an environment variable using `.bashrc`, follow these steps:

6. Open your terminal.
7. Edit the `.bashrc` file using a text editor like `nano` or `vim`. For example:
   ```bash
   nano ~/.bashrc
   ```
8. Add the following line at the end of the file, replacing "your_github_token_here" with your actual GitHub token:

```bash
export GITHUB_TOKEN="your_github_token_here"
```
9. Save the file and exit the text editor.
10. Reload the .bashrc file to apply the changes:
```bash
source ~/.bashrc
```
11. Now the GITHUB_TOKEN environment variable is set and can be used in your terminal sessions.
This configuration ensures that your GitHub token is securely stored as an environment variable and can be accessed by applications or scripts that need it.


