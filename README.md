# Dependency Release Tracker

![Dependency Release Tracker](https://github.com/hugovanderlei/SPM-Release-Tracker/assets/184836/7f31905f-2674-45ab-bf39-ab14f54d43bd)

## Overview
Dependency Release Tracker is a comprehensive tool designed to help developers keep track of package dependencies across various programming ecosystems, including Swift Package Manager (SPM) and Flutter. It lists release notes of dependencies directly within your project, helping you stay informed about updates and changes.

## Features
- **Cross-platform Support**: Track dependencies for **Swift, Flutter**, and potentially more platforms.
- **Enhanced Output Options**:
  - **Default Mode**: Lists only packages that have updates different from the ones locked in your project.
  - **`--all` Option**: Displays release notes for all versions of the dependencies.
  - **`--simple` Option**: Outputs a simplified list without detailed release notes.

## Installation

### Prerequisites
Ensure you have Python installed. You can install Python via Homebrew on macOS:
```bash
brew install python
```

## Installation

To install Python via Homebrew on macOS, run:
```bash
brew install python
```
This installs the latest Python version. Verify the installation with `python3 --version`.


### Tool Installation

Install pipx if not already installed:
```bash
brew install pipx
pipx ensurepath
```
Install Dependency Release Tracker:
```bash
pipx install dependency-release-tracker
```

## Upgrade
To upgrade to the latest version of `dependency-release-tracker`:

```bash
pipx upgrade dependency-release-tracker
```

## GitHub Token (Swift Projects Only)
For private repositories or to increase API rate limit, a GitHub token is required:

1. Go to [GitHub settings](https://github.com/settings/tokens).
2. Navigate to "Developer settings" > "Personal access tokens".
3. Click "Generate new token", give it a name, set an expiration, and select the `repo` scope.
4. Click "Generate token" and copy the generated token.
5. Save it securely and set it as an environment variable:

To set the GitHub token as an environment variable using `.bashrc`, or  follow these steps:

6. Open your terminal.
7. Edit the `.bashrc` or `.zshrc` file using a text editor like nano or vim. For example:

   ```bash
   nano ~/.bashrc
   ```
   or
   ```bash
   nano ~/.zshrc
   ```
   
9. Add the following line at the end of the file, replacing `"your_github_token_here"` with your actual GitHub token:

```bash
export GITHUB_TOKEN="your_github_token_here"
```
9. Save the file and exit the text editor.
10. Reload the `.bashrc` ou `.zshrc` file to apply the changes:
```bash
source ~/.bashrc
```
or 
```bash
source ~/.zshrc
```

11. Now the GITHUB_TOKEN environment variable is set and can be used in your terminal sessions.
This configuration ensures that your GitHub token is securely stored as an environment variable and can be accessed by applications or scripts that need it.

## Usage
Ensure you are in the root directory of your project:

- For **Swift projects**, this is the directory containing the .xcworkspace.
- For **Flutter projects**, ensure both pubspec.yaml and pubspec.lock are present.

Then execute:
```bash
dependency-tracker
```
Options:

- `--all` to see all versions.
- `--simple` for a simplified output.
- `--path` <path_to_directory> to specify the project directory if not the current directory.
- `--help` to display usage information.
- `--version` to display the current version.

## License
Pulse is available under the MIT license. See the LICENSE file for more info.


