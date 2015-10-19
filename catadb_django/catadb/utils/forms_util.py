from catadb.mysqldb import mysqldb as db
import crypt
from unicode_util import to_unicode


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
            'sight' - json
            'nose' - json
            'taste' - json
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

    # Wine type: red/white
    typed = args['type']

    # General information
    general_info = {}
    keys = ['country', 'appellation', 'grape', 'climate']
    for key in keys:
        if key in args:
            var = to_unicode(args[key])
            var = var.lower()
        else:
            var = u""
        general_info[key] = var

    # Sight
    sight = {}
    keys = ['clarity', 'brightness', 'concentration', 'color',
            'hue', 'rim', 'stain', 'tears', 'gas', 'sediment']
    for key in keys:
        if key in args:
            var = to_unicode(args[key])
            var = var.lower()
        else:
            var = u""
        sight[key] = var

    # Nose
    nose = {}
    keys = ['clean', 'intensity', 'age']
    for key in keys:
        if key in args:
            var = to_unicode(args[key])
            var = var.lower()
        else:
            var = u""
        nose[key] = var
    subkeys = ['fruit', 'nonfruit', 'organic', 'inorganic', 'wood']
    for subkey in subkeys:
        dict_ = {}
        for key in args:
            if 'nose_' + subkey in key:
                dict_[key] = to_unicode(args[key])
                dict_[key] = dict_[key].lower()
        nose[subkey] = dict_ 

    # Palate
    taste = {}
    keys = ['sweetness', 'body', 'texture', 'tannin', 'acid', 'alcohol',
            'structure_notes', 'length', 'complexity', 'balance']
    for key in keys:
        if key in args:
            var = to_unicode(args[key])
            var = var.lower()
        else:
            var = u""
        taste[key] = var    
    subkeys = ['fruit', 'nonfruit', 'organic', 'inorganic', 'wood']
    for subkey in subkeys:
        dict_ = {}
        for key in args:
            if 'taste_' + subkey in key:
                dict_[key] = to_unicode(args[key])
                dict_[key] = dict_[key].lower()
        taste[subkey] = dict_ 

    wine_data = {
        'name': name,
        'typed': typed,
        'pics': pics,
        'general_info': general_info,
        'sight': sight,
        'nose': nose,
        'taste': taste,
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
                     winedata['sight'],
                     winedata['nose'],
                     winedata['taste'],
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
            'sight' - json
            'nose' - json
            'taste' - json
            'notes' - unicode

    Output:
       wine_data - dict
            'name' - unicode
            'pics' - json
            'general_info' - json
            'intensities_taste' - json
            'intensities_nose' - json
            'sight' - json
            'nose' - json
            'taste' - json
            'notes' - unicode
    """
    if wine['pics']['front_label']:
       wine['pics']['front_label'] = "/" + wine['pics']['front_label']
       
    if wine['pics']['back_label']:
       wine['pics']['back_label'] = "/" + wine['pics']['back_label']

    # intensities:
    intensities_nose = {}
    try:
        intensities_nose['fruit_intensity'] = wine['nose']['fruit'].pop('nose_fruit_intensity')
    except:
        intensities_nose['fruit_intensity'] = u""
    try:
        intensities_nose['nonfruit_intensity'] = wine['nose']['nonfruit'].pop('nose_nonfruit_intensity')
    except:
        intensities_nose['nonfruit_intensity'] = u""
    try:
        intensities_nose['organic_intensity'] = wine['nose']['organic'].pop('nose_organic_intensity')
    except:
        intensities_nose['organic_intensity'] = u""
    try:
        intensities_nose['inorganic_intensity'] = wine['nose']['inorganic'].pop('nose_inorganic_intensity')
    except:
        intensities_nose['inorganic_intensity'] = u""

    intensities_taste = {}
    try:
        intensities_taste['fruit_intensity'] = wine['taste']['fruit'].pop('taste_fruit_intensity')
    except:
        intensities_taste['fruit_intensity'] = u""
    try:
        intensities_taste['nonfruit_intensity'] = wine['taste']['nonfruit'].pop('taste_nonfruit_intensity')
    except:
        intensities_taste['nonfruit_intensity'] = u""
    try:
        intensities_taste['organic_intensity'] = wine['taste']['organic'].pop('taste_organic_intensity')
    except:
        intensities_taste['organic_intensity'] = u""
    try:
        intensities_taste['inorganic_intensity'] = wine['taste']['inorganic'].pop('taste_inorganic_intensity')
    except:
        intensities_taste['inorganic_intensity'] = u""

    nose = {}
    nose['fruit_character'] = []
    fruit_characters = ['nose_fruit_tart', 'nose_fruit_overripe',
                        'nose_fruit_ripe', 'nose_fruit_baked']
    for key in fruit_characters:
        if key in wine['nose']['fruit']:
            val = wine['nose']['fruit'].pop(key)
            nose['fruit_character'].append({
                'val': val,
            }) 
    keys = ['fruit', 'nonfruit', 'organic', 'inorganic', 'wood']
    for key in keys:
        data = wine['nose'].pop(key)
        var_names = [x for x in data if "_notes" not in x]
        nose[key] = []
        for var_name in var_names:
            if var_name+"_notes" in data:
                dict_ = {
                    'val': data[var_name].title(),
                    'notes': data[var_name+"_notes"]
                }
            else:
                dict_ = {
                    'val': data[var_name].title(),
                }
            nose[key].append(dict_)

    nose.update(wine['nose'])

    taste = {}
    taste['fruit_character'] = []
    fruit_characters = ['taste_fruit_tart', 'taste_fruit_overripe',
                        'taste_fruit_ripe', 'taste_fruit_baked']
    for key in fruit_characters:
        if key in wine['taste']['fruit']:
            val = wine['taste']['fruit'].pop(key)
            taste['fruit_character'].append({
                'val': val,
            }) 
    keys = ['fruit', 'nonfruit', 'organic', 'inorganic', 'wood']
    for key in keys:
        data = wine['taste'].pop(key)
        var_names = [x for x in data if "_notes" not in x]
        taste[key] = []
        for var_name in var_names:
            if var_name+"_notes" in data:
                dict_ = {
                    'val': data[var_name].title(),
                    'notes': data[var_name+"_notes"]
                }
            else:
                dict_ = {
                    'val': data[var_name].title(),
                }                
            taste[key].append(dict_)
   
    taste.update(wine['taste'])


    templatedata = {
        'name': wine['name'].title(),
        'pics': wine['pics'],
        'notes': wine['notes'],
        'general_info': wine['general_info'],
        'intensities_taste': intensities_taste,
        'intensities_nose': intensities_nose,
        'sight': wine['sight'],
        'nose': nose,
        'taste': taste,
    }

    return templatedata
