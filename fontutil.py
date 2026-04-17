if __package__:
    from .nameutil import Names
else:
    from nameutil import Names

SUPERSCRIPTS = str.maketrans(
    "231ohɦjrɹɻʁwy ɣlsxʕნAÆBDEƎGHIJKLMNOȢPRTUWaɐɑᴂbdeəɛɜgkmŋoɔᴖᴗptuᴝɯvᴥβγδφχɒcɕðɜɟɥɨɩɪᵻʝɭᶅʟɱɰɲɳɴɵɸʂʃƫʉʊᴜʋʌʐʑʒθ0i456789+−=()nъьꝯĦœꜧꬷɫꭒ一二三四上中下甲乙丙丁天地人",
    "²³¹ºʰʱʲʳʴʵʶʷʸ˙ˠˡˢˣˤჼᴬᴭᴮᴰᴱᴲᴳᴴᴵᴶᴷᴸᴹᴺᴼᴽᴾᴿᵀᵁᵂᵃᵄᵅᵆᵇᵈᵉᵊᵋᵌᵍᵏᵐᵑᵒᵓᵔᵕᵖᵗᵘᵙᵚᵛᵜᵝᵞᵟᵠᵡᶛᶜᶝᶞᶟᶡᶣᶤᶥᶦᶧᶨᶩᶪᶫᶬᶭᶮᶯᶰᶱᶲᶳᶴᶵᶶᶷᶸᶹᶺᶼᶽᶾᶿ⁰ⁱ⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿꚜꚝꝰꟸꟹꭜꭝꭞꭟ㆒㆓㆔㆕㆖㆗㆘㆙㆚㆛㆜㆝㆞㆟",
)
SUBSCRIPTS = str.maketrans(
    "βγρφχ0123456789+−=()aeoxəhijklmnoprstuvx",
    "ᵦᵧᵨᵩᵪ₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓₔₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ",
)
BOLD = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗",
)  # SERIF BOLD
DOUBLE_STRUCK = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡",
)
FRAKTUR = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅",
)
ITALIC = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁",
)  # SERIF BOLD ITALIC
SQUARED = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉",
)
NEGATIVE_SQUARED = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉",
)
CIRCLED = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*/=\\問幼文箏ᄀᄂᄃᄅᄆᄇᄉᄋᄌᄎᄏᄐᄑᄒ가나다라마바사아자차카타파하우一二三四五六七八九十月火水木金土日株有社名特財祝労秘男女適優印注項休写正上中下左右医宗学監企資協夜アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヰヱヲ",
    "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ⓪①②③④⑤⑥⑦⑧⑨⊕⊖⊛⊘⊜⦸㉄㉅㉆㉇㉠㉡㉢㉣㉤㉥㉦㉧㉨㉩㉪㉫㉬㉭㉮㉯㉰㉱㉲㉳㉴㉵㉶㉷㉸㉹㉺㉻㉾㊀㊁㊂㊃㊄㊅㊆㊇㊈㊉㊊㊋㊌㊍㊎㊏㊐㊑㊒㊓㊔㊕㊖㊗㊘㊙㊚㊛㊜㊝㊞㊟㊠㊡㊢㊣㊤㊥㊦㊧㊨㊩㊪㊫㊬㊭㊮㊯㊰㋐㋑㋒㋓㋔㋕㋖㋗㋘㋙㋚㋛㋜㋝㋞㋟㋠㋡㋢㋣㋤㋥㋦㋧㋨㋩㋪㋫㋬㋭㋮㋯㋰㋱㋲㋳㋴㋵㋶㋷㋸㋹㋺㋻㋼㋽㋾",
) | {
    "10": "⑩",
    "11": "⑪",
    "12": "⑫",
    "13": "⑬",
    "14": "⑭",
    "15": "⑮",
    "16": "⑯",
    "17": "⑰",
    "18": "⑱",
    "19": "⑲",
    "20": "⑳",
    "21": "㉑",
    "22": "㉒",
    "23": "㉓",
    "24": "㉔",
    "25": "㉕",
    "26": "㉖",
    "27": "㉗",
    "28": "㉘",
    "29": "㉙",
    "30": "㉚",
    "31": "㉛",
    "32": "㉜",
    "33": "㉝",
    "34": "㉞",
    "35": "㉟",
    "36": "㊱",
    "37": "㊲",
    "38": "㊳",
    "39": "㊴",
    "40": "㊵",
    "41": "㊶",
    "42": "㊷",
    "43": "㊸",
    "44": "㊹",
    "45": "㊺",
    "46": "㊻",
    "47": "㊼",
    "48": "㊽",
    "49": "㊾",
    "50": "㊿",
}
NEGATIVE_CIRCLED = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩⓿➊➋➌➍➎➏➐➑➒",
) | {"11": "⓫", "12": "⓬", "13": "⓭", "14": "⓮", "15": "⓯", "16": "⓰", "17": "⓱", "18": "⓲", "19": "⓳", "20": "⓴"}
BLACKBOARD_BOLD = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ",
)  # UNICODE规范名称: BLACK-LETTER
SCRIPT = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵",
)
SCRIPT_BOLD = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩",
)
SANS_SERIF_BOLD = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵",
)
SANS_SERIF_BOLD_ITALIC = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕",
)
SANS_SERIF_ITALIC = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡",
)
FULLWIDTH_FORMS = str.maketrans(
    "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ ",
    "！＂＃＄％＆＇（）＊＋，－．／０１２３４５６７８９：；＜＝＞？＠ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ［＼］＾＿｀ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ｛｜｝～\u3000",
)
PARENTHESIZED = str.maketrans(
    "abcdefghijklmnopqrstuvwxyz123456789ᄀᄂᄃᄅᄆᄇᄉᄋᄌᄎᄏᄐᄑᄒ가나다라마바사아자차카타파하주一二三四五六七八九十月火水木金土日株有社名特財祝労代呼学監企資協祭休自至",
    "⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵⑴⑵⑶⑷⑸⑹⑺⑻⑼㈀㈁㈂㈃㈄㈅㈆㈇㈈㈉㈊㈋㈌㈍㈎㈏㈐㈑㈒㈓㈔㈕㈖㈗㈘㈙㈚㈛㈜㈠㈡㈢㈣㈤㈥㈦㈧㈨㈩㈪㈫㈬㈭㈮㈯㈰㈱㈲㈳㈴㈵㈶㈷㈸㈹㈺㈻㈼㈽㈾㈿㉀㉁㉂㉃",
) | {"10": "⑽", "11": "⑾", "12": "⑿", "13": "⒀", "14": "⒁", "15": "⒂", "16": "⒃", "17": "⒄", "18": "⒅", "19": "⒆", "20": "⒇"}
MONOSPACE = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿",
)  # MONOSPACE SERIF同
SANS_SERIF = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫",
)
REGION_INDICATOR = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿")
SMALL_CAPS = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴩǫʀꜱᴛᴜᴠᴡxʏᴢ")  # SMALL_CAPS非正式名称
HORIZONTAL_BAR = str.maketrans("0123456789", " ▏▎▍▌▋▊▉██")
VERTICAL_BAR = str.maketrans("0123456789", " ▁▂▃▄▅▆▇██")
ROMAN = str.maketrans("IVXLCDM", "ⅠⅤⅩⅬⅭⅮⅯ")
SMALL = str.maketrans("ivxlcdm,.;:?!(){}#&*+-<>=\\$%@", "ⅰⅴⅹⅼⅽⅾⅿ﹐﹒﹔﹕﹖﹗﹙﹚﹛﹜﹟﹠﹡﹢﹣﹤﹥﹦﹨﹩﹪﹫")
OUTLINED = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", "𜳖𜳗𜳘𜳙𜳚𜳛𜳜𜳝𜳞𜳟𜳠𜳡𜳢𜳣𜳤𜳥𜳦𜳧𜳨𜳩𜳪𜳫𜳬𜳭𜳮𜳯𜳰𜳱𜳲𜳳𜳴𜳵𜳶𜳷𜳸𜳹")
SEGMENTED = str.maketrans("0123456789", "🯰🯱🯲🯳🯴🯵🯶🯷🯸🯹")
SERIF_ITALIC = str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍")
CURRENCY_SIGN = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "₳฿₵ĐɆ₣₲ⱧłJ₭Ⱡ₥₦Ø₱QⱤ₴₮ɄV₩ӾɎⱫ")  # m理应为小写，但是为了一致，此处使用大写
UPSIDE_DOWN = str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "ɐqɔpǝɟƃɥıɾʞlɯuodbɹsʇnʌʍxʎzⱯꓭƆꓷƎℲꓨHIſꓘꓶWNOԀꝹꓤSꓕꓵꓥMX⅄Z")
PERIOD = str.maketrans(
    "123456789",
    "⒈⒉⒊⒋⒌⒍⒎⒏⒐",
) | {"10": "⒑", "11": "⒒", "12": "⒓", "13": "⒔", "14": "⒕", "15": "⒖", "16": "⒗", "17": "⒘", "18": "⒙", "19": "⒚", "20": "⒛"}
DOUBLE_CIRCLE = str.maketrans("123456789", "⓵⓶⓷⓸⓹⓺⓻⓼⓽") | {"10": "⓾"}
QUATERS = str.maketrans("0123456789abcdefABCDEF", " ▘▖▌▝▀▞▛▗▚▄▙▐▜▟█▄▙▐▜▟█")  # 象限序: 左上 左下 右上 右下
CHESS = str.maketrans("KQRBNPkqrbnp", "♔♕♖♗♘♙♚♛♜♝♞♟")
POKER = str.maketrans("SCHDschd", "♠♣♥♦♤♧♡♢")
PLASTIC = str.maketrans("12345670", "♳♴♵♶♷♸♹♺")
DIE = str.maketrans("123456", "⚀⚁⚂⚃⚄⚅")
DINGBAT = str.maketrans("123456789", "➀➁➂➃➄➅➆➇➈") | {"10": "➉"}
DINGBAT_NEG = str.maketrans("123456789", "❶❷❸❹❺❻❼❽❾") | {"10": "❿"}
DINGBAT_NEG_SANSSERIF = str.maketrans("123456789", "➊➋➌➍➎➏➐➑➒") | {"10": "➓"}
IDC = {
    "LR": "⿰",
    "LL": "⿲",
    "UD": "⿱",
    "UU": "⿳",
    "RD": "⿸",
    "RU": "⿺",
    "LD": "⿹",
    "LU": "⿽",
    "OD": "⿵",
    "OR": "⿷",
    "OU": "⿶",
    "OL": "⿼",
    "OC": "⿴",
    "XX": "⿻",
    "MI": "⿾",
    "RO": "⿿",
    "SU": "㇯",
}
SUZHOU = str.maketrans("123456789", "〡〢〣〤〥〦〧〨〩") | {"10": "〸", "20": "〹", "30": "〺"}
COBS = {"10": "㉈", "20": "㉉", "30": "㉊", "40": "㉋", "50": "㉌", "60": "㉍", "70": "㉎", "80": "㉏"}
MONTH = {
    "1月": "㋀",
    "2月": "㋁",
    "3月": "㋂",
    "4月": "㋃",
    "5月": "㋄",
    "6月": "㋅",
    "7月": "㋆",
    "8月": "㋇",
    "9月": "㋈",
    "10月": "㋉",
    "11月": "㋊",
    "12月": "㋋",
}
HOUR = {
    "0点": "㍘",
    "1点": "㍙",
    "2点": "㍚",
    "3点": "㍛",
    "4点": "㍜",
    "5点": "㍝",
    "7点": "㍟",
    "8点": "㍠",
    "9点": "㍡",
    "10点": "㍢",
    "11点": "㍣",
    "12点": "㍤",
    "13点": "㍥",
    "14点": "㍦",
    "15点": "㍧",
    "16点": "㍨",
    "17点": "㍩",
    "18点": "㍪",
    "19点": "㍫",
    "20点": "㍬",
    "21点": "㍭",
    "22点": "㍮",
    "23点": "㍯",
    "24点": "㍰",
}
DAY = {
    "1日": "㏠",
    "2日": "㏡",
    "3日": "㏢",
    "4日": "㏣",
    "5日": "㏤",
    "6日": "㏥",
    "7日": "㏦",
    "8日": "㏧",
    "9日": "㏨",
    "10日": "㏩",
    "11日": "㏪",
    "12日": "㏫",
    "13日": "㏬",
    "14日": "㏭",
    "15日": "㏮",
    "16日": "㏯",
    "17日": "㏰",
    "18日": "㏱",
    "19日": "㏲",
    "20日": "㏳",
    "21日": "㏴",
    "22日": "㏵",
    "23日": "㏶",
    "24日": "㏷",
    "25日": "㏸",
    "26日": "㏹",
    "27日": "㏺",
    "28日": "㏻",
    "29日": "㏼",
    "30日": "㏽",
    "31日": "㏾",
}
YI = {
    "乾": "䷀",
    "坤": "䷁",
    "屯": "䷂",
    "蒙": "䷃",
    "需": "䷄",
    "讼": "䷅",
    "师": "䷆",
    "比": "䷇",
    "小畜": "䷈",
    "履": "䷉",
    "泰": "䷊",
    "否": "䷋",
    "同人": "䷌",
    "大有": "䷍",
    "谦": "䷎",
    "豫": "䷏",
    "随": "䷐",
    "蛊": "䷑",
    "临": "䷒",
    "观": "䷓",
    "噬嗑": "䷔",
    "贲": "䷕",
    "剥": "䷖",
    "复": "䷗",
    "无妄": "䷘",
    "大畜": "䷙",
    "颐": "䷚",
    "大过": "䷛",
    "坎": "䷜",
    "离": "䷝",
    "咸": "䷞",
    "恒": "䷟",
    "遁": "䷠",
    "大壮": "䷡",
    "晋": "䷢",
    "明夷": "䷣",
    "家人": "䷤",
    "睽": "䷥",
    "蹇": "䷦",
    "解": "䷧",
    "损": "䷨",
    "益": "䷩",
    "夬": "䷪",
    "姤": "䷫",
    "萃": "䷬",
    "升": "䷭",
    "困": "䷮",
    "井": "䷯",
    "革": "䷰",
    "鼎": "䷱",
    "震": "䷲",
    "艮": "䷳",
    "渐": "䷴",
    "归妹": "䷵",
    "丰": "䷶",
    "旅": "䷷",
    "巽": "䷸",
    "兑": "䷹",
    "涣": "䷺",
    "节": "䷻",
    "中孚": "䷼",
    "小过": "䷽",
    "既济": "䷾",
    "未济": "䷿",
}
MIRROR = str.maketrans("()[]{}<>bdpq/", ")(][}{><dbqp\\")


fonts: Names[dict[int, int] | dict[int | str, int | str] | dict[str, str]] = Names()
fonts.name(SUPERSCRIPTS, "上标", "sup")
fonts.name(SUBSCRIPTS, "下标", "sub")
fonts.name(BOLD, "粗体", "黑体", "bold", "b", "衬线粗体", "衬线粗体字符", "衬线粗体字母", "serifbold", "sb")
fonts.name(DOUBLE_STRUCK, "双线", "双线体", "doublestruck")
fonts.name(FRAKTUR, "fraktur", "fraktur体", "粗哥特体", "哥特粗体", "德文黑体", "花体", "粗黑板粗体")
fonts.name(
    ITALIC,
    "斜体",
    "意大利体",
    "意大利斜体",
    "italic",
    "i",
    "衬线粗斜体",
    "衬线粗斜体字符",
    "衬线粗斜体字母",
    "衬线粗意大利体",
    "衬线意大利粗体",
    "serifbolditalic",
    "serifitalicbold",
    "sbi",
    "sib",
)
fonts.name(SQUARED, "方框", "带框字母", "带框字符", "sq", "square", "squared", "box", "boxed")
fonts.name(NEGATIVE_SQUARED, "黑底方框", "黑底带框字母", "黑底带框字符", "反白", "nsq", "negsquare", "negsquared", "negbox", "negboxed")
fonts.name(CIRCLED, "圆圈", "带圈字母", "带圈字符", "circle", "circ", "circled")
fonts.name(NEGATIVE_CIRCLED, "黑底圆圈", "黑底带圈字母", "黑底带圈字符", "反白圆圈", "ncirc", "negcircle", "negcircled")
fonts.name(BLACKBOARD_BOLD, "黑板粗体", "bb", "blackboard", "哥特体", "mathbb")
fonts.name(SCRIPT, "草书", "草书体", "手写", "手写体", "脚本", "script")
fonts.name(SCRIPT_BOLD, "粗草书", "粗草书体", "草书粗体", "粗手写", "粗手写体", "手写粗体", "粗脚本", "scriptbold")
fonts.name(SANS_SERIF_BOLD, "无衬线粗体", "ssbold", "ssb")
fonts.name(
    SANS_SERIF_BOLD_ITALIC,
    "无衬线粗斜体",
    "无衬线意大利粗体",
    "粗斜体",
    "粗斜",
    "意大利粗体",
    "ssbolditalic",
    "ssitalicbold",
    "ssbitalic",
    "ssibold",
    "ssbi",
    "ssib",
)
fonts.name(SANS_SERIF_ITALIC, "无衬线斜体", "无衬线意大利体", "ssitalic", "ssi")
fonts.name(
    FULLWIDTH_FORMS,
    "全角",
    "全角字符",
    "全角形式",
    "全角形式字符",
    "全角形式字母",
    "全形",
    "全形字母",
    "全形字符",
    "fw",
    "fs",
    "full",
    "fullwidth",
    "fullshape",
)
fonts.name(PARENTHESIZED, "括号", "带括号字母", "带括号字符", "par", "parenthesized")
fonts.name(
    MONOSPACE,
    "等宽",
    "等宽字符",
    "等宽形式",
    "等宽形式字符",
    "等宽形式字母",
    "mono",
    "monospace",
    "monospaced",
    "衬线",
    "衬线字符",
    "衬线形式",
    "衬线形式字符",
    "衬线形式字母",
    "serif",
)
fonts.name(SANS_SERIF, "无衬线", "无衬线字符", "无衬线形式", "无衬线形式字符", "无衬线形式字母", "ss", "sansserif")
fonts.name(REGION_INDICATOR, "区域指示符", "区域指示符字符", "区域指示符字母", "旗帜符号", "旗帜", "国旗", "reg", "flag", "region")
fonts.name(SMALL_CAPS, "小大写字母", "小大写", "sc", "smallcaps")
fonts.name(HORIZONTAL_BAR, "水平条", "横条", "水平进度条", "hbar")
fonts.name(VERTICAL_BAR, "垂直条", "竖条", "垂直进度条", "vbar")
fonts.name(ROMAN, "罗马数字", "罗马数字字符", "罗马数字字母", "roman")
fonts.name(SMALL, "小型", "小型字符", "小型字母", "小型数字", "small")
fonts.name(OUTLINED, "轮廓", "空心", "外框", "空心字符", "外框字符", "空心字母", "外框字母", "outlined", "ol")
fonts.name(SEGMENTED, "七段", "七段字符", "七段数字", "数码管", "segmented", "seg")
fonts.name(
    SERIF_ITALIC, "衬线斜体", "衬线斜体字符", "衬线斜体字母", "衬线意大利体", "衬线意大利体字符", "衬线意大利体字母", "serifitalic", "si"
)
fonts.name(CURRENCY_SIGN, "货币符号", "货币符号字符", "货币符号字母", "货币", "currency", "cs", "cur")
fonts.name(UPSIDE_DOWN, "倒置", "倒转", "颠倒", "颠倒字符", "颠倒字母", "颠倒数字", "颠倒符号", "ud", "upsidedown", "翻转")
fonts.name(PERIOD, "圆点", "圆点数字", "句点", "带点数字", "period", "dot", "dots")
fonts.name(DOUBLE_CIRCLE, "双圆圈", "双圆圈数字", "双圈", "双圈数字", "doublecircle", "doublecirc", "dcirc", "2circ")
fonts.name(QUATERS, "象限", "四象限", "quarters", "quart")
fonts.name(CHESS, "国象", "国际象棋", "chess")
fonts.name(POKER, "扑克", "扑克牌", "poker")
fonts.name(PLASTIC, "塑料", "塑料标号", "回收", "回收标号", "recycle", "plastic")
fonts.name(DIE, "骰子", "色子", "die", "dice")
fonts.name(DINGBAT, "筹码", "dingbat")  # 注: dingbat此处并不应当译为“筹码”，但是出于区分度等考虑，保留“筹码”的译法。
fonts.name(DINGBAT_NEG, "反白筹码", "negdingbat")
fonts.name(DINGBAT_NEG_SANSSERIF, "反白无衬线筹码", "无衬线筹码", "negdingbatss")
fonts.name(IDC, "表意文字描述符", "idc")
fonts.name(SUZHOU, "苏州码子", "sz", "suzhou")
fonts.name(COBS, "黑方块白圆圈", "黑底白圆圈", "方圆", "circleonblacksquare", "circleonnegsquare", "circonnegsq")
fonts.name(MONTH, "月", "月份", "month")
fonts.name(DAY, "日", "日期", "天", "day")
fonts.name(HOUR, "时", "小时", "hour")
fonts.name(YI, "易", "易经", "卦", "六十四卦", "yijing", "yi")
fonts.name(MIRROR, "镜像", "对称", "对称字符", "对称字母", "对称数字", "对称符号", "mirror", "symmetry")

RESERVED_BRAILLE = "⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿"  # 尚未决定应当将这些字符映射到哪些字符，因此保留备用。
