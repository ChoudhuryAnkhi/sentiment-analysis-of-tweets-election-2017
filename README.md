sklearn-senti-refactor
==============================

combine tweets about the German Federal Election 2017 and analyze sentiments for each of the candidates and their political parties.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org

    
Rudimentary data exploration
-----------------

1. column headings: 
    ```
    ## column indices
    #    (0, 'id')
    #    (1, 'time')
    #    (2, 'created_at')
    #    (3, 'from_user_name')
    #    (4, 'text')
    #    (5, 'filter_level')
    #    (6, 'possibly_sensitive')
    #    (7, 'withheld_copyright')
    #    (8, 'withheld_scope')
    #    (9, 'truncated')
    #    (10, 'retweet_count')
    #    (11, 'favorite_count')
    #    (12, 'lang')
    #    (13, 'to_user_name')
    #    (14, 'in_reply_to_status_id')
    #    (15, 'quoted_status_id')
    #    (16, 'source')
    #    (17, 'location')
    #    (18, 'lat')
    #    (19, 'lng')
    #    (20, 'from_user_id')
    #    (21, 'from_user_realname')
    #    (22, 'from_user_verified')
    #    (23, 'from_user_description')
    #    (24, 'from_user_url')
    #    (25, 'from_user_profile_image_url')
    #    (26, 'from_user_utcoffset')
    #    (27, 'from_user_timezone')
    #    (28, 'from_user_lang')
    #    (29, 'from_user_tweetcount')
    #    (30, 'from_user_followercount')
    #    (31, 'from_user_friendcount')
    #    (32, 'from_user_favourites_count')
    #    (33, 'from_user_listed')
    #    (34, 'from_user_withheld_scope')
    #    (35, 'from_user_created_at')
    ```
2. One liner to calculate number of different langugage tweets
    ```
    $ for file in `ls data/raw/*.csv`; do python -c "import csv; csvdata = open('$file','r'); print(\"\n\".join([ row[12] for row in csv.reader(csvdata)]))";done |  sort | uniq -c | sort -k1 -nr 
    4487616 de
    2021752 en
     272617 tr
     232340 es
     167390 fr
     136570 und
      92139 nl
      78496 pl
      65341 it
      41663 pt
      31331 in
      29222 ja
      17213 da
       8047 ro
       8005 et
       7919 sv
       7707 tl
       7533 cs
       6818 el
       6428 no
       5605 hu
       3994 fi
       3589 th
       3330 ht
       3050 ko
       2803 ru
       2771 sl
       1736 bn
       1546 ar
       1300 cy
       1083 lt
       1033 zh
        552 vi
        445 lv
        420 eu
        357 is
        216 hi
        202 lang
        188 fa
        171 uk
        137 iw
        132 bg
         85 sr
         57 ur
         10 ta
          7 km
          6 ne
          4 mr
          4 ml
          3 my
          3 ka
          3 am
          2 ckb
          1 te
      ```
3. Another interesting exploration is the number of tweets written by users identifying with lang2 in lang1. This gives us an estimate of how interesting to (possibly) bilinguals this topic is.  

    ```
    $ for file in `ls data/raw/*.csv`; do python -c "import csv; csvdata = open('$file','r'); print(\"\n\".join([ \" \".join([row[12],row[-8]]) for row in csv.reader(csvdata)]))";done |  sort | uniq -c | sort -k1 -nr 
        202 lang from_user_lang
    3878717 de de
    1650645 en en
     449555 de en
     237340 tr tr
     196574 es es
     134520 fr fr
     101293 en de
      70246 und de
      66543 pl pl
      53501 it it
      51128 en en-gb
      49907 nl nl
      47892 en es
      33278 pt pt
      30663 en fr
      28595 de ru
      28347 de nl
      27329 ja ja
      25680 und en
      24435 en nl
      23705 nl en
      23257 de es
      20535 es en
      19712 fr en
      18988 de en-gb
      17562 tr en
      17194 de fr
      17011 in en
      16569 en ru
      14337 nl de
      13182 de tr
      12673 und ca
      12543 en pl
      12484 en it
      12005 und es
      11804 tr de
      11574 en pt
       9909 en tr
       8054 en en-GB
       7755 pl en
       7381 da de
       6764 it en
       6607 en ja
       6297 pt en
       6191 es ca
       5760 tl en
       5579 en sv
       5489 de it
       4880 da en
       4607 fr de
       4530 ro en
       4403 en ca
       4071 de pl
       4032 de pt
       3945 in id
       3928 cs cs
       3885 et en
       3773 in en-gb
       3632 sv sv
       3586 en ar
       3324 el el
       3303 en id
       3235 el en
       3091 da da
       3056 in de
       2892 en ko
       2870 en el
       2828 sv en
       2815 es de
       2800 en da
       2754 no en
       2668 th th
       2642 de ja
       2617 und en-gb
       2478 fr en-gb
       2470 hu en
       2403 fr es
       2348 pl de
       2301 ko ko
       2235 no de
       2135 und nl
       2103 ht en-gb
       1955 en fi
       1933 cs en
       1891 sl en
       1813 ru ru
       1788 und ru
       1762 tr nl
       1736 bn en
       1725 fi fi
       1675 de cs
       1629 es pt
       1383 ja en
       1367 tr fr
       1359 en cs
       1354 et en-gb
       1270 und sr
       1267 nl en-gb
       1266 en th
       1229 de sv
       1225 de da
       1215 und fr
       1195 und pl
       1151 it es
       1107 de zh-cn
       1051 de ar
       1047 hu hu
        996 it de
        985 es fr
        952 et de
        940 en ro
        918 sv de
        917 fi en
        912 en no
        884 th en
        876 fr it
        874 es it
        841 tr ru
        838 und th
        838 de hu
        821 ar ar
        803 de no
        783 und tr
        777 ro ro
        776 pt es
        767 in es
        765 en uk
        765 de ca
        751 tl en-gb
        742 und pt
        705 de ko
        703 nl fr
        696 cs ru
        694 cy en-gb
        685 de xx-lc
        684 en zh-cn
        671 en hu
        660 it fr
        658 fr ru
        656 en hr
        633 ru de
        628 und it
        623 es en-gb
        618 it en-gb
        607 ar en
        600 de id
        580 hu de
        571 in fr
        554 tl de
        540 hu en-gb
        537 ro es
        536 nl ru
        522 fi en-gb
        514 ro de
        504 tr en-gb
        496 de el
        485 und hr
        481 und ja
        464 ht en
        451 lt de
        444 lt en
        436 nl es
        435 no no
        434 fr nl
        428 ko en
        422 en sr
        416 de en-GB
        408 es ja
        395 pt de
        390 de uk
        387 pl en-gb
        376 fr pt
        374 da nl
        370 pt en-gb
        369 in tr
        368 und ar
        362 es gl
        358 zh en
        340 et pt
        340 et ar
        339 in pl
        338 und el
        335 da en-gb
        325 en he
        324 ro tr
        323 es ru
        317 ht fr
        306 in it
        305 nl pt
        300 en zh-CN
        292 it pt
        290 ht de
        288 de fi
        285 pl fr
        283 cy en
        278 tr ar
        275 fi de
        272 hu tr
        262 sl sr
        260 ro it
        256 da es
        254 et tr
        253 fr pl
        249 it id
        245 ja de
        244 ru en
        244 en vi
        243 hu es
        239 in ru
        237 in nl
        233 it bg
        231 in pt
        230 vi vi
        229 et es
        221 en fa
        217 zh zh-cn
        217 eu de
        216 tr es
        216 is de
        215 en zh-tw
        214 pl es
        214 lv en
        212 nl tr
        210 vi en
        210 und cs
        210 pt fr
        204 no pl
        204 fr ja
        203 ro fr
        201 en lv
        196 en xx-lc
        195 pl tr
        194 sl en-gb
        194 es eu
        191 it ru
        191 de ro
        184 et fr
        183 de vi
    ```
--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
