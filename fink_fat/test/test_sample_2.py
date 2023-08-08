import pandas as pd


local_orbit_test = pd.DataFrame(
    {
        "trajectory_id": [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
        ],
        "provisional designation": [
            "K22J00A",
            "K22J00B",
            "K22J00C",
            "K22J00D",
            "K22J00E",
            "K22J00F",
            "K22J00G",
            "K22J00H",
            "K22J00J",
            "K22J00K",
            "K22J00L",
            "K22J00M",
            "K22J00N",
            "K22J00O",
            "K22J00P",
            "K22J00Q",
            "K22J00R",
            "K22J00S",
            "K22J00T",
            "K22J00U",
            "K22J00V",
            "K22J00W",
            "K22J00X",
            "K22J00Y",
            "K22J00Z",
            "K22J01A",
            "K22J01B",
            "K22J01C",
            "K22J01D",
            "K22J01E",
        ],
        "ref_epoch": [
            2459711.757999841,
            2459711.757062341,
            2459711.763196541,
            2459715.678011341,
            2459711.756587741,
            2459715.679018341,
            2459713.672803041,
            -1.0,
            2459715.733740541,
            2459715.737641041,
            2459711.672895641,
            2459711.901425741,
            2459711.980106341,
            2459711.762722041,
            2459714.742247541,
            2459715.679018341,
            2459714.907259041,
            2459711.763196541,
            2459715.690592441,
            2459715.674724341,
            2459711.773451241,
            2459711.756587741,
            2459714.975997541,
            2459712.992606341,
            2459714.820071541,
            2459714.975997541,
            2459714.975997541,
            2459714.737860941,
            2459712.923138741,
            2459714.690858641,
        ],
        "a": [
            2.854626945860004,
            2.8400018381355254,
            2.349115790802076,
            2.985603816761514,
            2.9501610179948425,
            3.436285239687775,
            2.529525698493788,
            -1.0,
            2.687683768614495,
            3.724303209452564,
            4.718329825072936,
            27.45983613989412,
            0.4131150149887037,
            1.3348515163409718,
            1.6564554404532683,
            2.0280704185110725,
            1.1878730252238734,
            3.170340493460828,
            2.335294290101059,
            3.2496954870615777,
            2.716435594636384,
            3.2329495136374886,
            1.0702265841642582,
            1.5752124498428444,
            5.240101663194289,
            0.7718968173432424,
            1.1694468508448408,
            1.8584324897551263,
            3.797909560478512,
            2.164211072948916,
        ],
        "e": [
            0.054386031711898,
            0.222135230115363,
            0.05878828706904,
            0.020445682097639,
            0.438261088942304,
            0.207190598583934,
            0.156773161133555,
            -1.0,
            0.164051056063237,
            0.392268733678186,
            0.401602273788382,
            0.953997399126203,
            0.956261979329515,
            0.434660218730765,
            0.253439494143259,
            0.926413193972278,
            0.150927345214668,
            0.193581676960837,
            0.148407780880723,
            0.201918809160895,
            0.195244004510233,
            0.390020601401493,
            0.137731428077707,
            0.455437681202125,
            0.902300587906382,
            0.322907708519991,
            0.155540477896752,
            0.613853248962727,
            0.534272222214196,
            0.162943113031552,
        ],
        "i": [
            13.349892000701,
            12.7083018921375,
            4.4042271974487,
            13.3050015907204,
            1.7146637779252,
            5.5385629837075,
            11.6486171043441,
            -1.0,
            16.7551827956172,
            2.3332562334812,
            8.2913124173516,
            8.3205557181995,
            86.3120545096365,
            7.4560911820028,
            24.1223226992667,
            17.9793541173623,
            79.7019607979053,
            2.6567559656908,
            12.8245216258889,
            15.0299348985664,
            12.2864354818431,
            3.5165148690074,
            2.992601210816,
            8.351150775483,
            35.2329256543221,
            3.337649393717,
            1.8476650035936,
            5.5863109768936,
            6.9511726348887,
            10.0860874464809,
        ],
        "long. node": [
            101.1077168498739,
            181.7170795996844,
            208.290025569426,
            111.8530194887455,
            168.0852731386908,
            258.5048173990712,
            182.0446969880643,
            -1.0,
            253.2055250296727,
            313.2009746251849,
            228.6672926444379,
            168.6753699013202,
            96.8179701984228,
            144.6885695192242,
            68.2498251583832,
            348.0624888363685,
            64.8981903901968,
            92.5087886928521,
            263.5363947175751,
            242.4877525976243,
            269.4229836294855,
            184.0655282150567,
            207.7080507828008,
            221.2099399225111,
            60.8500108293774,
            67.7644582956092,
            227.2781308099142,
            140.9504843065524,
            200.0458290456558,
            335.368071005816,
        ],
        "arg. peric": [
            301.1892705751906,
            109.1124617580614,
            267.3445795721806,
            220.3074391159112,
            224.9448673600392,
            261.0904280801848,
            117.1835708550172,
            -1.0,
            10.0726812234544,
            229.3732105629425,
            349.4326560645083,
            29.854985324963,
            348.9185362797142,
            224.4255551738858,
            338.6271832526673,
            28.5392203504697,
            204.7492190438277,
            326.2405842305226,
            4.9320891217446,
            313.1252141081754,
            15.7050974800072,
            58.6435404816164,
            63.9642459804768,
            55.9671477888039,
            272.5083743707499,
            12.2525526954462,
            33.416937922232,
            149.1368315199433,
            359.3164785382573,
            24.059834922501,
        ],
        "mean anomaly": [
            128.0504702301497,
            265.6772020175563,
            56.7023012251359,
            201.9632221128267,
            100.9621348550511,
            11.2039180614993,
            258.762978260363,
            -1.0,
            313.7508939673487,
            359.1262635948422,
            341.6203184434197,
            0.4837165622125,
            127.4409481989369,
            165.4338597180254,
            125.2372151766679,
            51.8219953198186,
            333.9348020193385,
            83.5646660770372,
            314.4899330167115,
            1.6494393529177,
            303.4616088754953,
            333.577939634307,
            334.7207208794387,
            345.7766283891943,
            355.950905444186,
            136.8798783116385,
            341.2187500343535,
            325.997335187273,
            12.9456266375809,
            188.2177076423483,
        ],
        "rms_a": [
            1.30358,
            1.6674,
            2.16548e-155,
            2.23465,
            2.15728e-155,
            4.16774,
            0.918363,
            -1.0,
            0.264775,
            2.15726e-155,
            5.95519,
            2.15419e-155,
            2.15948e-155,
            2.16156e-155,
            0.110014,
            2.16002e-155,
            2.16077e-155,
            2.15686e-155,
            0.162486,
            0.441794,
            0.304153,
            2.15749e-155,
            2.96093,
            2.1642e-155,
            2.16554e-155,
            2.15932e-155,
            2.15958e-155,
            2.1613e-155,
            0.931575,
            2.1626899999999998e-155,
        ],
        "rms_e": [
            0.547823,
            0.216715,
            2.16548e-155,
            0.393856,
            2.15728e-155,
            0.702551,
            0.131857,
            -1.0,
            0.108996,
            2.15726e-155,
            0.786904,
            2.15419e-155,
            2.15948e-155,
            2.16156e-155,
            0.0490097,
            2.16002e-155,
            2.16077e-155,
            2.15686e-155,
            0.0839206,
            0.0944248,
            0.14198,
            2.15749e-155,
            2.57106,
            2.1642e-155,
            2.16554e-155,
            2.15932e-155,
            2.15958e-155,
            2.1613e-155,
            0.143641,
            2.1626899999999998e-155,
        ],
        "rms_i": [
            0.630719,
            1.12651,
            8.6335e-155,
            1.92204,
            8.6335e-155,
            0.494484,
            0.889854,
            -1.0,
            0.564529,
            8.6335e-155,
            0.700955,
            8.6335e-155,
            8.6335e-155,
            8.6335e-155,
            1.00609,
            8.6335e-155,
            8.6335e-155,
            8.6335e-155,
            0.393494,
            0.637415,
            0.385951,
            8.6335e-155,
            18.6096,
            8.6335e-155,
            8.6335e-155,
            8.6335e-155,
            8.6335e-155,
            8.6335e-155,
            0.519776,
            8.6335e-155,
        ],
        "rms_long. node": [
            15.0283,
            1.11667,
            3.8206400000000003e-160,
            19.8341,
            3.8206400000000003e-160,
            23.0023,
            0.967445,
            -1.0,
            2.12361,
            3.8206400000000003e-160,
            7.07463,
            3.8206400000000003e-160,
            3.8206400000000003e-160,
            3.8206400000000003e-160,
            3.17407,
            3.8206400000000003e-160,
            3.8206400000000003e-160,
            3.8206400000000003e-160,
            1.88076,
            2.25387,
            2.41417,
            3.8206400000000003e-160,
            180.685,
            3.8206400000000003e-160,
            3.8206400000000003e-160,
            3.8206400000000003e-160,
            3.8206400000000003e-160,
            3.8206400000000003e-160,
            2.56402,
            3.8206400000000003e-160,
        ],
        "rms_arg. peric": [
            97.9446,
            141.165,
            4.02731e-159,
            2100.65,
            4.02731e-159,
            229.253,
            132.87,
            -1.0,
            3.78668,
            4.02731e-159,
            11.2522,
            4.02731e-159,
            4.02731e-159,
            4.02731e-159,
            9.26196,
            4.02731e-159,
            4.02731e-159,
            4.02731e-159,
            1.04945,
            39.2864,
            10.3819,
            4.02731e-159,
            319.234,
            4.02731e-159,
            4.02731e-159,
            4.02731e-159,
            4.02731e-159,
            4.02731e-159,
            7.25558,
            4.02731e-159,
        ],
        "rms_mean anomaly": [
            69.2811,
            187.353,
            0.0,
            2182.88,
            0.0,
            155.01,
            163.524,
            -1.0,
            13.3545,
            0.0,
            38.2106,
            0.0,
            0.0,
            0.0,
            8.71873,
            0.0,
            0.0,
            0.0,
            9.11557,
            25.4535,
            24.4056,
            0.0,
            246.421,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            4.57889,
            0.0,
        ],
        "chi_reduced": [
            0.9249999523162842,
            0.4733333587646484,
            -1.0,
            1.2159999847412108,
            -1.0,
            1.8337500095367432,
            1.5230000495910645,
            -1.0,
            1.329999923706055,
            -1.0,
            1.558750033378601,
            -1.0,
            -1.0,
            -1.0,
            2.0322223239474826,
            -1.0,
            -1.0,
            -1.0,
            1.0612499713897705,
            1.5422222349378798,
            1.7249999046325684,
            -1.0,
            0.1337499916553497,
            -1.0,
            -1.0,
            -1.0,
            -1.0,
            -1.0,
            1.8333333333333333,
            -1.0,
        ],
        "last_ra": [
            162.7899399,
            155.0203048,
            154.3769627,
            159.9437485,
            161.5256864,
            155.1379396,
            161.6777631,
            173.7325891,
            174.8582455,
            155.3094573,
            154.8386596,
            286.3608979,
            358.3890907,
            155.9521342,
            176.5912368,
            155.0411549,
            310.3961378,
            149.9467818,
            181.9197656,
            174.4085353,
            185.5063392,
            160.9430171,
            4.6212897,
            7.124997,
            253.0940513,
            2.7586555,
            0.9080898,
            141.6943942,
            258.6303249,
            161.579828,
        ],
        "last_dec": [
            23.131125,
            8.0960537,
            7.8809133,
            22.4741937,
            8.0860086,
            3.528951,
            7.6690483,
            58.5014025,
            -18.4494694,
            8.0419729,
            2.3087531,
            -6.154138,
            16.7487622,
            16.4154416,
            32.0889501,
            6.0833443,
            34.0062292,
            15.1204273,
            -19.4625573,
            -13.297781,
            -19.9769673,
            8.125872,
            17.565801,
            23.3494954,
            8.1513294,
            17.5999796,
            18.341969,
            20.1965079,
            -13.2474502,
            0.9738753,
        ],
        "last_jd": [
            2459715.7132523,
            2459715.7368403,
            2459715.7373148,
            2459715.7146644,
            2459715.7368403,
            2459715.7368403,
            2459715.7368403,
            2459715.7636111,
            2459715.7329398,
            2459715.7368403,
            2459715.7373148,
            2459713.9399074,
            2459713.979456,
            2459715.7146644,
            2459715.719537,
            2459715.7368403,
            2459714.9645718,
            2459715.7377778,
            2459715.7320023,
            2459715.7546065,
            2459715.7305671,
            2459715.7368403,
            2459714.979213,
            2459714.9884606,
            2459714.8586111,
            2459714.9771991,
            2459714.979213,
            2459714.7375347,
            2459714.8553125,
            2459715.7368403,
        ],
        "last_mag": [
            18.462766647338867,
            18.949522018432617,
            17.627470016479492,
            17.855350494384766,
            18.989574432373047,
            18.62224578857422,
            16.664573669433594,
            18.566835403442383,
            17.330028533935547,
            18.8760929107666,
            19.121341705322266,
            13.055002212524414,
            18.384183883666992,
            18.713520050048828,
            18.840383529663086,
            18.556589126586914,
            18.344196319580078,
            15.862868309020996,
            18.399614334106445,
            16.89029312133789,
            16.2099666595459,
            18.155574798583984,
            18.274776458740234,
            16.570165634155273,
            17.714719772338867,
            15.062811851501465,
            18.53762435913086,
            16.043930053710938,
            13.988967895507812,
            19.25284194946289,
        ],
        "last_fid": [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            2,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            2,
            2,
            2,
            2,
            2,
            1,
            2,
            1,
        ],
    }
)


cluster_mode_cli_test = pd.DataFrame(
    {
        "trajectory_id": {0: 0, 1: 1, 2: 3, 3: 2},
        "ref_epoch": {
            0: 2459714.980013741,
            1: 2459714.977999841,
            2: 2459714.980013741,
            3: 2459714.980013741,
        },
        "a": {
            0: 1.0702265437866862,
            1: 0.7718967868550072,
            2: 3.291412522664472,
            3: 1.1694447970375377,
        },
        "e": {
            0: 0.13773139413248,
            1: 0.322907773731163,
            2: 0.721156065972337,
            3: 0.155538888520195,
        },
        "i": {
            0: 2.9926010000725,
            1: 3.3376504744254,
            2: 6.7127544889377,
            3: 1.8476516840565,
        },
        "long. node": {
            0: 207.7080483819948,
            1: 67.7644544508514,
            2: 223.8846721769481,
            3: 227.2780754156898,
        },
        "arg. peric": {
            0: 63.9642506926364,
            1: 12.2525559261523,
            2: 38.0542689846552,
            3: 33.4169876651417,
        },
        "mean anomaly": {
            0: 334.7242925207828,
            1: 136.8827844308033,
            2: 357.2935595556638,
            3: 341.2218198218268,
        },
        "rms_a": {0: 2.96093, 1: 2.16177e-155, 2: 2.16292e-155, 3: 2.15674e-155},
        "rms_e": {0: 2.57106, 1: 2.16177e-155, 2: 2.16292e-155, 3: 2.15674e-155},
        "rms_i": {0: 18.6096, 1: 8.6335e-155, 2: 8.6335e-155, 3: 8.6335e-155},
        "rms_long. node": {
            0: 180.685,
            1: 3.82064e-160,
            2: 3.82064e-160,
            3: 3.82064e-160,
        },
        "rms_arg. peric": {
            0: 319.234,
            1: 4.02731e-159,
            2: 4.02731e-159,
            3: 4.02731e-159,
        },
        "rms_mean anomaly": {0: 246.406, 1: 0.0, 2: 0.0, 3: 0.0},
        "chi_reduced": {0: 0.13374999165534973, 1: -1.0, 2: -1.0, 3: -1.0},
        "last_ra": {0: 4.6212897, 1: 2.7586555, 2: 0.1999204, 3: 0.9080898},
        "last_dec": {0: 17.565801, 1: 17.5999796, 2: 18.6658829, 3: 18.341969},
        "last_jd": {
            0: 2459714.979213,
            1: 2459714.9771991,
            2: 2459714.979213,
            3: 2459714.979213,
        },
        "last_mag": {
            0: 18.274776458740234,
            1: 15.062811851501465,
            2: 19.020517349243164,
            3: 18.53762435913086,
        },
        "last_fid": {0: 2, 1: 2, 2: 2, 3: 2},
    }
)
