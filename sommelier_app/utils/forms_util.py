from mysqldb import mysqldb as db
from utils import crypt
from utils.unicode_util import to_unicode


def process_forms(args):
    """
    take args from POST request (tasting_notes) and 
    build a dictionary

    Input:
        args:  arguments from POST request
        userid: unicode - uuid

    Output:
        wine_data - dict
            'name' - unicode
            'typed' - unicode
            'pics' - json
            'general_info' - json
            'fruit_family' - json
            'fruit_quality' - json
            'non_fruit_quality' - json
            'structure' - json
            'notes' - unicode
    """
    # Name of Wine    
    name = u""
    if 'name' in args:
        name = to_unicode(args['name'])
        name = name.lower()

    # Address where the pictures are stored in the server
    pics = args['pics']

    # notes
    notes = args['notes']
    notes = to_unicode(notes)

    # Fruit quality
    fruit_quality = {}
    try:
        fruit_quality['tart'] = args['tart']
    except:
        fruit_quality['tart'] = '0'

    try:
        fruit_quality['ripe'] = args['ripe']
    except:
        fruit_quality['ripe'] = '0'

    try:
        fruit_quality['overripe'] = args['overripe']
    except:
        fruit_quality['overripe'] = '0'

    try:
        fruit_quality['baked'] = args['baked']
    except:
        fruit_quality['baked'] = '0'

    # General info:
    general_info = {}
    try:
        # 1 - cool/moderate
        # 2 - warm/hot
        general_info['climate'] = args['climate']
    except:
        general_info['climate'] = '0'
        
    try:
        # 1 - new world
        # 2 - old world
        general_info['style'] = args['style']
    except:
        general_info['style'] = '0'

    try:
        # 1 - 1-3 years
        # 2 - 4-6 years
        # 3 - 7+ years
        general_info['age'] = args['age']
    except:
        general_info['age'] = '0'

    try:
        general_info['country'] = to_unicode(args['country'])
    except:
        general_info['country'] = u""

    typed = args['type']

    if typed == 'red':
        try:
            # 1 - Cavernet Sauv or Merlot
            # 2 - Syrah/shiraz
            # 3 - pinot noir o rgamay
            # 4 - tempranillo or grenache
            # 5 - sangiovese or nebbiolo
            # 6 - malbec or zinfandel
            general_info['grape'] = args['grape']
        except:
            general_info['grape'] = '0'

        try:
            # 1 - garnet
            # 2 - ruby
            # 3 - purple
            general_info['color'] = args['color']
        except:
            general_info['color'] = '0'

        # Fruit Family
        fruit_family = {}
        try:
            fruit_family['red'] = args['red']
        except:
            fruit_family['red'] = '0'

        try:
            fruit_family['black'] = args['black']
        except:
            fruit_family['black'] = '0'

        try:
            fruit_family['blue'] = args['blue']
        except:
            fruit_family['blue'] = '0'

        try:
            fruit_family['fig_raisin'] = args['fig_raisin']
        except:
            fruit_family['fig_raisin'] = '0'

        # Non-Fruit quality
        nonfruit_quality = {}
        try:
            nonfruit_quality['flowers'] = args['flowers']
        except:
            nonfruit_quality['flowers'] = '0'

        try:
            nonfruit_quality['vegetal'] = args['vegetal']
        except:
            nonfruit_quality['vegetal'] = '0'

        try:
            nonfruit_quality['herbs'] = args['herbs']
        except:
            nonfruit_quality['herbs'] = '0'

        try:
            nonfruit_quality['peppercorn'] = args['peppercorn']
        except:
            nonfruit_quality['peppercorn'] = '0'

        try:
            nonfruit_quality['vanilla'] = args['vanilla']
        except:
            nonfruit_quality['vanilla'] = '0'

        try:
            nonfruit_quality['game'] = args['game']
        except:
            nonfruit_quality['game'] = '0'

        try:
            nonfruit_quality['balsamic'] = args['balsamic']
        except:
            nonfruit_quality['balsamic'] = '0'

        try:
            nonfruit_quality['organic_earth'] = args['organic_earth']
        except:
            nonfruit_quality['organic_earth'] = '0'

        try:
            nonfruit_quality['inorganic_earth'] = args['inorganic_earth']
        except:
            nonfruit_quality['inorganic_earth'] = '0'

        try:
            nonfruit_quality['oak'] = args['oak']
        except:
            nonfruit_quality['oak'] = '0'

        # Structure
        structure = {}
        try:
            # 1. dry
            # 2. off dry
            # 3. sweet
            structure['sweet'] = args['sweet']
        except:
            structure['sweet'] = '0'

        try:
            structure['tannin'] = args['tannin']
        except:
            structure['tannin'] = '0'

        try:
            structure['acid'] = args['acid']
        except:
            structure['acid'] = '0'

        try:
            structure['alcohol'] = args['alcohol']
        except:
            structure['alcohol'] = '0'

    # white wine
    else:
        try:
            # 1 - Chenin Blanc or Pinot Gris
            # 2 - Pinot Grigio
            # 3 - Riesling or Albarino
            # 4 - Chardonnay
            # 5 - Gewurz or Torrontes
            # 6 - Sauvignon Blanc
            general_info['grape'] = args['grape']
        except:
            general_info['grape'] = '0'

        try:
            # 1 - straw
            # 2 - yellow
            # 3 - gold
            general_info['color'] = args['color']
        except:
            general_info['color'] = '0'

        # Fruit Family
        fruit_family = {}
        try:
            fruit_family['apple_pear'] = args['apple_pear']
        except:
            fruit_family['apple_pear'] = '0'

        try:
            fruit_family['citrus'] = args['citrus']
        except:
            fruit_family['citrus'] = '0'

        try:
            fruit_family['pitted_stone'] = args['pitted_stone']
        except:
            fruit_family['pitted_stone'] = '0'

        try:
            fruit_family['tropical'] = args['tropical']
        except:
            fruit_family['tropical'] = '0'

        try:
            fruit_family['melon'] = args['melon']
        except:
            fruit_family['melon'] = '0'

        # Non-Fruit quality
        nonfruit_quality = {}
        try:
            nonfruit_quality['flowers'] = args['flowers']
        except:
            nonfruit_quality['flowers'] = '0'

        try:
            nonfruit_quality['vegetal'] = args['vegetal']
        except:
            nonfruit_quality['vegetal'] = '0'

        try:
            nonfruit_quality['ginger'] = args['ginger']
        except:
            nonfruit_quality['ginger'] = '0'

        try:
            nonfruit_quality['vanilla'] = args['vanilla']
        except:
            nonfruit_quality['vanilla'] = '0'

        try:
            nonfruit_quality['yeast'] = args['yeast']
        except:
            nonfruit_quality['yeast'] = '0'

        try:
            nonfruit_quality['butter'] = args['butter']
        except:
            nonfruit_quality['butter'] = '0'

        try:
            nonfruit_quality['organic_earth'] = args['organic_earth']
        except:
            nonfruit_quality['organic_earth'] = '0'

        try:
            nonfruit_quality['inorganic_earth'] = args['inorganic_earth']
        except:
            nonfruit_quality['inorganic_earth'] = '0'

        try:
            nonfruit_quality['oak'] = args['oak']
        except:
            nonfruit_quality['oak'] = '0'

        # Structure
        structure = {}
        try:
            # 1. dry
            # 2. off dry
            # 3. sweet
            structure['sweet'] = args['sweet']
        except:
            structure['sweet'] = '0'

        try:
            structure['bitter_phenolic'] = args['bitter_phenolic']
        except:
            structure['bitter_phenolic'] = '0'

        try:
            structure['acid'] = args['acid']
        except:
            structure['acid'] = '0'

        try:
            structure['alcohol'] = args['alcohol']
        except:
            structure['alcohol'] = '0'

    wine_data = {
        'name': name,
        'typed': typed,
        'pics': pics,
        'general_info': general_info,
        'fruit_family': fruit_family,
        'fruit_quality': fruit_quality,
        'non_fruit_quality': nonfruit_quality,
        'structure': structure,
        'notes': notes,
    }

    return wine_data 


def store_wine_data(args, userid):
    """
    store the extracted data from the tasting notes in 
    the Database

    Input:
        args:  arguments from POST request
        userid: unicode - uuid

    Output:
        bool:  true if correct.
    """
    winedata = process_forms(args)

    wdb = db.Wines()
    res = wdb.insert(userid,
                     winedata['name'],
                     winedata['typed'],
                     winedata['pics'],
                     winedata['general_info'],
                     winedata['fruit_family'],
                     winedata['fruit_quality'],
                     winedata['non_fruit_quality'],
                     winedata['structure'],
                     winedata['notes'])
    if res:
        return True

    return False


def compose_wine_data_for_template(wine):
    """
    massage the data to get it ready to render
    the wine compose_wine_data_for_template

    Input:
        wine_data - dict
            'name' - unicode
            'typed' - unicode
            'pics' - json
            'general_info' - json
            'fruit_family' - json
            'fruit_quality' - json
            'non_fruit_quality' - json
            'structure' - json
            'notes' - unicode

    Output:
       wine_data - dict
            'name' - unicode
            'typed' - unicode
            'pics' - json
            'general_info' - json
            'fruit_family' - json
            'fruit_quality' - json
            'non_fruit_quality' - json
            'structure' - json
            'notes' - unicode
    """
    values = ["", "Dominant", "Slight/None"]
    values3 = ["", "Low to Moderate Minus", "Moderate to Moderate Plus", "High"]

    # Fruit quality
    fruit_quality = [
        {
            'key': 'Tart',
            'value': values[int(wine['fruit_quality']['tart'])],
        },
        {
            'key': 'Ripe',
            'value': values[int(wine['fruit_quality']['ripe'])],
        },
        {
            'key': 'Overripe/Jammy/Cooked',
            'value': values[int(wine['fruit_quality']['overripe'])],
        },
        {
            'key': 'Baked/Dried/Oxidized',
            'value': values[int(wine['fruit_quality']['baked'])],
        },
    ]

    # General info:
    general_info = {}
    climate = ["", "Cool/Moderate", "Warm/Hot"]
    general_info['climate'] = climate[int(wine['general_info']['climate'])]
        
    style = ["", "New World", "Old World"]
    general_info['style'] = style[int(wine['general_info']['style'])]

    age = ["", "1-3 Years", "4-6 Years", "7+ Years"]
    general_info['age'] = age[int(wine['general_info']['age'])]

    general_info['country'] = wine['general_info']['country'].title()


    if wine['typed'] == 'red':
        grapes = ["", "Cavernet Sauv or Merlot", "Syrah/shiraz",
                  "Pinot Noir o Rgamay", "Tempranillo or Grenache",
                  "Sangiovese or Nebbiolo", "Malbec or Zinfandel"]
        general_info['grape'] = grapes[int(wine['general_info']['grape'])]

        color = ["", "Garnet", "Ruby", "Purple"]
        general_info['color'] = color[int(wine['general_info']['color'])]

        # Fruit Family
        fruit_family = [
            {
                'key': 'Red',
                'value': values[int(wine['fruit_family']['red'])],
            },
            {
                'key': 'Black',
                'value': values[int(wine['fruit_family']['black'])],
            },
            {
                'key': 'Blue',
                'value': values[int(wine['fruit_family']['blue'])],
            },
            {
                'key': 'Fig/Raisin',
                'value': values[int(wine['fruit_family']['fig_raisin'])],
            },
        ]

        # Non-Fruit quality
        nonfruit_quality = [
            {
                'key': 'Aromatic Flowers',
                'value': values[int(wine['non_fruit_quality']['flowers'])],
            },
            {
                'key': 'Vegetal, Green Pepper',
                'value': values[int(wine['non_fruit_quality']['vegetal'])],
            },
            {
                'key': 'Fresh/Dried Herbs, Mint, Eucalyptus',
                'value': values[int(wine['non_fruit_quality']['herbs'])],
            },
            {
                'key': 'Peppercorn',
                'value': values[int(wine['non_fruit_quality']['peppercorn'])],
            },                        
            {
                'key': 'Vanilla, Smoke, Toast, Coconut',
                'value': values[int(wine['non_fruit_quality']['vanilla'])],
            },
            {
                'key': 'Game, Blood, Cured Meat, Leather',
                'value': values[int(wine['non_fruit_quality']['game'])],
            },
            {
                'key': 'Balsamic, Tar',
                'value': values[int(wine['non_fruit_quality']['balsamic'])],
            },
        ]

        nonfruit_quality_2 = [
            {
                'key': '<b>Organic Earth:</b> Wet Leaves, Brett, Mushrooms',
                'value': values[int(wine['non_fruit_quality']['organic_earth'])],
            },
            {
                'key': '<b>Inorganic Earth:</b> Stone, Rock, Mineral, Sulfur',
                'value': values[int(wine['non_fruit_quality']['inorganic_earth'])],
            },
            {
                'key': '<b>Oak:</b> Was this wine aged in noticeale new oak?',
                'value': values[int(wine['non_fruit_quality']['oak'])],
            },
        ]

        # Structure
        sweetness = ["", "Dry", "Off Dry", "Sweet"]
        sweet = sweetness[int(wine['structure']['sweet'])]

        structure = [
            {
                'key': 'Tannin',
                'value': values3[int(wine['structure']['tannin'])],
            },
            {
                'key': 'Acid',
                'value': values3[int(wine['structure']['acid'])],
            },
            {
                'key': 'Alcohol',
                'value': values3[int(wine['structure']['alcohol'])],
            },
        ]

    # white wine
    else:
        grapes = ["", "Chenin Blanc or Pinot Gris", "Pinot Grigio",
                  "Riesling or Albarino", "Chardonnay",
                  "Gewurz or Torrontes", "Sauvignon Blanc"]
        general_info['grape'] = grapes[int(wine['general_info']['grape'])]

        color = ["", "Straw", "Yellow", "Gold"]
        general_info['color'] = color[int(wine['general_info']['color'])]

        # Fruit Family
        fruit_family = [
            {
                'key': 'Apple/Pear',
                'value': values[int(wine['fruit_family']['apple_pear'])],
            },
            {
                'key': 'Citrus',
                'value': values[int(wine['fruit_family']['citrus'])],
            },
            {
                'key': 'Pitted/Stone',
                'value': values[int(wine['fruit_family']['pitted_stone'])],
            },
            {
                'key': 'Tropical',
                'value': values[int(wine['fruit_family']['tropical'])],
            },
            {
                'key': 'Melon',
                'value': values[int(wine['fruit_family']['melon'])],
            },
        ]

        # Non-Fruit quality
        nonfruit_quality = [
            {
                'key': 'Aromatic Flowers',
                'value': values[int(wine['non_fruit_quality']['flowers'])],
            },
            {
                'key': 'Distinctive Herbal or Vegetal Notes',
                'value': values[int(wine['non_fruit_quality']['vegetal'])],
            },
            {
                'key': 'Ginger, Honey, Wax, Botrytis',
                'value': values[int(wine['non_fruit_quality']['ginger'])],
            },
            {
                'key': 'Vanilla, Brown Baking Spice, Smoke, Toast',
                'value': values[int(wine['non_fruit_quality']['vanilla'])],
            },                        
            {
                'key': 'Yeast, Dough, Baked Bread',
                'value': values[int(wine['non_fruit_quality']['yeast'])],
            },
            {
                'key': 'Butter, Cream',
                'value': values[int(wine['non_fruit_quality']['butter'])],
            },
        ]

        nonfruit_quality_2 = [
            {
                'key': '<b>Organic Earth:</b> Wet Leaves, Brett, Mushrooms',
                'value': values[int(wine['non_fruit_quality']['organic_earth'])],
            },
            {
                'key': '<b>Inorganic Earth:</b> Stone, Rock, Mineral, Sulfur',
                'value': values[int(wine['non_fruit_quality']['inorganic_earth'])],
            },
            {
                'key': '<b>Oak:</b> Was this wine aged in noticeale new oak?',
                'value': values[int(wine['non_fruit_quality']['oak'])],
            },
        ]

        # Structure
        sweetness = ["", "Dry", "Off Dry", "Sweet"]
        sweet = sweetness[int(wine['structure']['sweet'])]

        structure = [
            {
                'key': 'Bitter, Phenolic Finish',
                'value': values3[int(wine['structure']['bitter_phenolic'])],
            },
            {
                'key': 'Acid',
                'value': values3[int(wine['structure']['acid'])],
            },
            {
                'key': 'Alcohol',
                'value': values3[int(wine['structure']['alcohol'])],
            },
        ]

    templatedata = {
        'name': wine['name'].title(),
        'pics': wine['pics'],
        'notes': wine['notes'],
        'general_info': general_info,
        'fruit_family': fruit_family,
        'fruit_quality': fruit_quality,
        'non_fruit_quality': nonfruit_quality,
        'non_fruit_quality_2': nonfruit_quality_2,
        'sweet': sweet,
        'structure': structure,
    }

    return templatedata
