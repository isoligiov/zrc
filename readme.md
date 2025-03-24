1. Pre-requisite ( Adjust Zoom app setting )
- Tick `Keep me signed in` when signing into the account.
- In `Settings/Video` tab
  * uncheck `Always display participant name on their videos`.
  * check `Stop my video when joining`.
- In `Settings/Audio` tab
  * check `Automatically join computer audio when joining`.
  * check `Mute my mic when joining`.
- In `Settings/Share screen` tab
  * select `Automatically share desktop` of `When I share my screen in a meeting` item.
  * go to `Advanced` item and uncheck `Show green border around the shared content`
2. How to install
```bash
./install.sh
# After module installation, it will require APP_NAME
# Input APP_NAME which will be the unique identifier. i.e. amazon
```
3. How to run
```bash
./run.sh
```