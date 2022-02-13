# flyers2

This is a my hobby script:)
collect flyers from stores website and post to your slack.

## how to use

```
# git clone <this repo>
# cd <dir>
# cp config_example.ini config.ini
    -> <set "your slack token" and "target shopurls" to config.ini>
# python -m flyers2
```
 -> post flyers to your slack channels :clap:

## Workable flyers sites

### tokubai

https://tokubai.co.jp/

### kurashiru

https://chirashi.kurashiru.com/

### yorkmart

https://www.york-inc.com/

### yaoko

https://www.yaoko-net.com/

### rogers

https://www.rogers.co.jp/


## Caution

if you want to set URLEncoded url to `target.shops`,  
you need to set the % to two  
ex)  
`https://%E3%83%A8%E3%83` -> `https://%%E3%%83%%A8%%E3%%83`
