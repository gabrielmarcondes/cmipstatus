from settings import officeboy_configs as config
from .tupa_bots.quaco.tests import errorcodes
import os
import glob


def get_tupa_data():
    """
    retrieves the running stats
    """
    log_file = open(config['qstat_log'], 'r')
    log_text = log_file.readlines()
    log_file.close()
    return log_text


def get_readme():
    """
    retrieves the readme info
    """
    readme_file = open(config['readme'], 'r')
    readme_text = readme_file.readlines()
    readme_file.close()
    return readme_text


def get_restart_list(fancy_name):
    """
    retrieves the restart list for a given exp/member
    """
    fancy_filename = config['restart_list_template'].format(fancy_name)
    try_again = False
    # special case for unique member with _1
    if '_' not in fancy_name:
        fancy_alt = config['restart_list_template'].format(fancy_name+'_1')
        try_again = True

    try:
        restart_file = open(fancy_filename, 'r')
    except:
        if try_again:
            try:
                restart_file = open(fancy_alt, 'r')
            except:
                raise Exception
        else:
            raise Exception

    restart_list = restart_file.readlines()
    restart_file.close()
    return restart_list


def get_fc_log():
    fc_log = open(config['fc_log'], 'r')
    lines = fc_log.readlines()
    fc_log.close()
    log = []
    for line in lines:
        columns = line.split(',')
        filename = os.path.basename(columns[0])
        #error_description = errorcodes.descriptions[int(columns[1])]
        error_description = errorcodes.decode(int(columns[1]))
        log.append({'file': filename, 'error': error_description})
    return log
        

def get_figs_for(exp, member):
    folder = '{0}_{1}'.format(exp, '%.2d' % member)
    media_folder = config['figures'].format(folder)
    figs = {}
    if os.path.exists(media_folder):
        gifs = sorted(os.listdir(media_folder))
        gifs = [g for g in gifs if '.gif' in g]
        for g in gifs: #expanding list comprehension for the sake of beauty
            name = g[:-4].split('-')[1]
            path = os.path.join(folder, g)
            figs[name] = figs.get(name, []) + [path]
    return figs


def get_cmip_figs(decadal):
    figs = glob.glob(config['cmip_figures'])
    figs_structure = {}
    decadal = 'decadal' + decadal
    figs = [f for f in sorted(figs) if decadal in f]
    for fig in figs:
        fig_name = os.path.basename(fig)
        parts = fig_name.split('-')
        var = parts[1]
        rip = parts[4]

        if not figs_structure.has_key(var):
            figs_structure[var] = []

        figs_structure[var].append(fig_name)

    return figs_structure
        
