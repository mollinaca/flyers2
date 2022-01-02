# flyers2

Scripts to collect flyers from stores and post to slack.
This is a script for my hobby.

## how to use

```
# git clone <this repo>
# cd <dir>
# cp config_example.ini config.ini
# <set up your slack token and target shopurls>
# python -m flyers2
```
 -> post flyers to your slack channels :clap:

## Workable flyers pages

### tokubai

https://tokubai.co.jp/

### kurashiru

https://chirashi.kurashiru.com/

## Caution

if you want to set URLEncoded url to `target.shops`,  
you need to set the % to two  
ex)  
`https://%E3%83%A8%E3%83` -> `https://%%E3%%83%%A8%%E3%%83`
