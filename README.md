# osufetch
Little program, that show your osu profile info like neofetch/fastfetch

<img width="657" height="930" alt="image" src="https://github.com/user-attachments/assets/4ebdc053-7537-45a9-9319-89bf182560eb" />

## Installation

### Arch Linux
Use your preffered AUR helper to install [osufetch](https://aur.archlinux.org/packages/osufetch-bin)
```
yay -S osufetch-bin
```
```
paru -S osufetch-bin
```

### Other distros
Use this command to start installation script
```
curl -s https://raw.githubusercontent.com/kartavkun/osufetch/main/install.sh | bash
```

## Usage

### How to Use
Type `osufetch` in your terminal

Then will starts first run setup, and you need to enter your OAuth client id and secret, then id of your osu! profile (https://osu.ppy.sh/users/{id})

After the first run setup, you can use `osufetch` command to show your osu profile info

Also you can use `osufetch --id {id}` to show info about specific osu! profile

### How to get your OAuth client id and secret
Go to [osu!](https://osu.ppy.sh/home/account/edit) and click on "New OAuth Application" button

Then type any name of your application and click on "Create" button

You will get Client ID and Client Secret, that you need to enter in osufetch setup

Client ID, Client Secret and your osu! profile id will be saved in `~/.config/osufetch/config.ini`

Then you will be redirected to [osu!](https://osu.ppy.sh/oauth/applications) and click on "Create" button

## To-do
Nothing :3
