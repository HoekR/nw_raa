#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from collections import defaultdict


table_dict = defaultdict(dict)
for table in common_tables:
    for periode in transposed_graph[table]:
        periode = periode.strip().replace(' ', '_')
        tname = '_'.join([periode, table]).strip()
        print(f"getting {tname}")
        dftable = pd.read_sql_table(con="mysql+pymysql://rik:X0chi@localhost/raa_old", table_name=tname)
        dftable = dftable.rename(columns={c:c.lower() for c in dftable.columns})
        print(f"adding {table.lower()} to {periode}")
        table_dict[periode][table.lower()] = dftable


common_tables = [t.lower() for t in common_tables]
common_tables


for tb in table_dict['batfra'].keys():
    print(f"""'{tb}': '{','.join([c.lower() for c in table_dict['batfra'][tb].columns])}',""")



ids = {'AcademischeTitel': ['IDAcademischeTitel'],
'AdellijkeTitel': ['IDAdellijkeTitel'],
'aliassen': ['IDPersoon'],
'Bron': ['IDBron'],
'BronFunctieDetails': ['IDBron','IDBovenLokaalCollegeRegentDetails'],
'BronRegentDetails': ['IDRegent','IDBron'],
'College': ['IDCollege','Id'],
'Functie': ['IDFunctie','Id'],
'FunctieBovenLokaal': ['ID FunctieBovenLokaal'],
'FunctieLokaal': ['ID FunctieLokaal'],
'lokaal': ['IDlokaal'],
'provinciaal': ['IDprovincie'],
'Regent': ['IDRegent', 'IDAdellijkeTitel','IDAcademischeTitel'],
'regionaal': ['IDregio', 'IDRegio'],
'stand': ['IDstand'],
'BovenLokaalCollegeRegentDetails': ['ID','IDRegent','IDFunctie','IDCollege'],
'Gewest': ['IDGewest'],}

nids = {}
for k in ids.keys():
    v = [x.lower() for x in ids[k]]
    nids[k.lower()] = v
nids



idmappings = defaultdict(list)
joined_tables = {}
for tbl in common_tables:
    for key in table_dict.keys():
        if tbl in table_dict[key].keys():
            addtbl = table_dict[key][tbl]
        else:
            print (f"no {tbl} in {key}")
        try:
            for idnr in nids.get(tbl):
                addtbl[f'old_{idnr}'] = addtbl[idnr].apply(lambda x: f"{key}_{x}")
                idmappings[f'old_{idnr}'].append(tbl)
        except (KeyError, TypeError):
            print (f"no {idnr} on {tbl} in {key}")
        if tbl in joined_tables.keys():
            print(f"joining {key}, {tbl}")
            joined_tables[tbl] = pd.concat([joined_tables[tbl],addtbl])
        else:
            joined_tables[tbl] = addtbl


ids = nids
ids


addtbl.columns


# In[1537]:


joined_tables.keys()


# In[1539]:


joined_tables['regent']


# In[1541]:


outdir = "/Users/rikhoekstra/PycharmProjects/nw_raa/convert_raa/original/brondata/rawconvert"
try:
    os.makedirs(outdir)
except FileExistsError:
    pass
for key in joined_tables.keys():
    dfout = joined_tables[key]
    dfout.to_csv(os.path.join(outdir, key + '.csv'))
    


# In[1542]:


uniqtitels


# wat willen we eigenlijk weten:
# 
# - gegeven een tbl met daarin titel, titelid, oude titel willen we hebben unieke titel, unieke id, referentie naar oude titel
# - dus idealiter oude titel  -> nieuwe id, nieuwe titel
# - daarom moeten we hebben unieke lijst van titels
# - daaruit genereren we een unieke lijst van titels + id
# - we voegen die dan toe aan de tabel waarin die titel wordt gerefereerd

# In[1548]:


at = joined_tables['academischetitel']
at


# In[1550]:


uniqtitels = pd.DataFrame(list(at.academischetitel.unique()), columns=['academischetitel'])
uniqtitels['nwnr'] = uniqtitels.index

nwtitels = pd.merge(left=uniqtitels, right=at[['old_idacademischetitel', 'academischetitel']], on='academischetitel')


# In[1551]:


adelstitels = joined_tables['adellijketitel']


# In[1552]:


persoon = joined_tables['regent']
persoon.reset_index(inplace=True) # because it keeps the original indexes of the old tables
persoon


# In[1553]:


nr = 6
nwtitels.loc[nwtitels.old_idacademischetitel==f'batfra_{nr}']


# In[1554]:


columnlist = list(persoon.columns)+['nwnr']
columnlist


# In[1555]:


# so generalize

# we have a number of tables that are referenced

idmappings = {i:list(set(idmappings[i])) for i in idmappings.keys()}
idmappings


# In[1556]:


def get_unique(tbln, column):
    tbl = njoined_tables[tbln]
    uniqtitels = pd.DataFrame(list(tbl[tbln].unique()), columns=[tbln])
    uniqtitels['nwnr'] = uniqtitels.index

    nwtitels = pd.merge(left=uniqtitels, right=tbl[[column, tbln]], on=tbln)

    print(tbl.columns, column)
    return nwtitels


# In[1557]:


graph=idmappings
transposed_graph = defaultdict(list)
for node, neighbours in graph.items():
    for neighbour in neighbours:
        transposed_graph[neighbour.lower()].append(node.lower())
transposed_graph


# In[1558]:


reftables =['academischetitel',
 'adellijketitel',
 'bron',
 'college',
 'functie',
 'functiebovenLokaal',
 'functielokaal',
 'lokaal',
 'gewest',
 'regent',
 'stand']


# In[1559]:


references = {}
reftables = [r.lower() for r in reftables]
for tbln in reftables:
    try:
        print(f"trying to get {column} from {transposed_graph[tbln]}")
        column = [v for v in transposed_graph[tbln] if tbln in v][0]
        print ('gelukt')
    except (IndexError, KeyError):
        print('fout', tbln, transposed_graph[tbln])
        continue
    try:
        print(f"trying to get_unique {column} from {tbln}")
        references[tbln] = get_unique(tbln, column)
        print('this worked\n----------')
    except KeyError:
        print('fout getting unique', tbln, transposed_graph[tbln])
        continue


# In[1560]:


joined_tables['regent']


# In[1569]:


transposed_graph.keys()


# In[1570]:


nwetabellen = {}
for tbln in transposed_graph.keys():
    if tbln not in reftables:
        worktable = joined_tables[tbln]
        for reference in transposed_graph[tbln]:
            print (reference, transposed_graph[tbln])
            tn = [v for v in transposed_graph[tbln] if v == reference][0]
            #print('tn: ', tn)
            rtbl = tn.replace('old_ID','')
            workreference = references.get(rtbl)
            #print ('workreference: ', workreference)
            if workreference is not None:
                print (f"updating {tbln} with {rtbl}, column {reference}")
                columnlist = list(worktable.columns)+[f'{rtbl.lower()}_id']
                worktable = worktable.merge(workreference, on=reference, how='left')
            #worktable.rename(columns={'nwnr':'academischetitel_id'}, inplace=True)
        worktable
        nwetabellen[tbln]=worktable
    else:
        nwetabellen[tbln] = joined_tables[tbln]


# In[1564]:


tbln = 'bovenlokaalcollegeregentdetails'
if tbln not in reftables:
    worktable = joined_tables[tbln]
    for reference in transposed_graph[tbln]:
        print (reference, transposed_graph[tbln])
        tn = [v for v in transposed_graph[tbln] if v == reference][0]
        #print('tn: ', tn)
        rtbl = tn.replace('old_ID','')
        workreference = references.get(rtbl)
        #print ('workreference: ', workreference)
        if workreference is not None:
            print (f"updating {tbln} with {rtbl}, column {reference}")
            columnlist = list(worktable.columns)+[f'{rtbl.lower()}_id']
            worktable = worktable.merge(workreference, on=reference, how='left')
        #worktable.rename(columns={'nwnr':'academischetitel_id'}, inplace=True)
    worktable


# In[1572]:


nwetabellen.keys()


# In[1566]:


nwetabellen['bovenlokaalcollegeregentdetails'].columns


# In[ ]:





# In[1574]:


outdir = "/Users/rikhoekstra/PycharmProjects/nw_raa/convert_raa/original/brondata/rawmerge"
try: 
    os.makedirs(outdir)
except FileExistsError:
    pass
for key in nwetabellen.keys():
    dfout = joined_tables[key]
    dfout.to_csv(os.path.join(outdir, key + '.csv'), sep="\t")
    


# In[1580]:


regent.rename(columns={"heerlijkheid": "old_heerlijkheid"}, inplace=True)


# In[1583]:


regent['heerlijkheid'] = regent.old_heerlijkheid + ' en ' + regent.heerlijkheid2
regent.heerlijkheid


# In[1618]:


regent["filled_geboortedag"] = regent.geboortedag.fillna(1).astype(int).fillna(1)
regent["filled_geboortemaand"] = regent.geboortemaand.fillna(1).astype(int).fillna(1)
regent["filled_geboortejaar"] = regent.geboortejaar.fillna(0).astype(int).fillna(0)


# In[1701]:


from string import Template
datum = "{jaar:04d}-{maand:02d}-{dag:02d}"

print(datum.format(jaar=200, maand=1,dag=3))
pd.Period(datum.format(jaar=200, maand=1,dag=3), freq="D")

def my_conv(x):
    try:
        return pd.Period(x, freq="D")
    except ValueError:
        pass

def try_padding(possible_int):
    try:
        possible_int = int(possible_int)
        return '%02d'%possible_int
    except ValueError as e:
        if not np.isnan(possible_int):
            return possible_int


# In[1683]:


regent.geboortedatum_als_bekend = regent.apply(lambda x: '-'.join([try_padding(d) for d in [
                        x.geboortejaar, x.geboortemaand, x.geboortedag ] if d and not np.isnan(d)]),
                        axis=1)


# In[1702]:


for j in ["overlijdensdag", "overlijdensmaand", "overlijdensjaar"]:
    regent[j] = regent[j].astype(int, errors="ignore")


# In[1718]:


regent.overlijdensjaar.loc[regent.overlijdensjaar.str.contains('?',
                            regex=False, na=False)].str.replace('?','9')


# In[1709]:


regent.overlijdensdatum_als_bekend = regent.apply(lambda x: '-'.join([try_padding(d) for d in [
                        x.overlijdensjaar, x.overlijdensmaand, x.overlijdensdag ] if d and d==d]),
                        axis=1)


# In[1707]:


regent.overlijdensjaar.isna()


# In[1687]:


rec = regent.iloc[7810]


# In[1692]:


rec.overlijdensjaar.dtype


# In[1681]:


tgd.loc[~regent.geboortemaand.isna()]


# In[1670]:


tgd.apply(lambda x: '-'.join([try_padding(d) for d in [
                        x.geboortedag, x.geboortemaand, x.geboortejaar] if d]),
                        axis=1)


# In[1632]:


regent.columns


# In[1576]:


def regent_to_persoon():

    # list of heerlijkheden
    if data.heerlijkheid:
        heerlijkheden = data.heerlijkheid
        if data.heerlijkheid2:
            heerlijkheden = heerlijkheden + ' en ' + data.heerlijkheid2
    else:
        heerlijkheden = ''

    known_geboortedatum = '-'.join(
        [try_padding(d) for d in [
            data.geboortedag, data.geboortemaand, data.geboortejaar] if d])
    geboortedatum = stringToDate(
        data.geboortejaar, data.geboortemaand, data.geboortedag
        )

    doopjaar = (data.doopjaar == '1')

    known_overlijdensdatum = '-'.join(
        [try_padding(d) for d in [
            data.overlijdensdag, data.overlijdensmaand, data.overlijdensjaar] if d]
        )
    overlijdensdatum = stringToDate(
        data.overlijdensjaar, data.overlijdensmaand, data.overlijdensdag,
        as_end_date=True
        )

    if data.adellijketitel and             data.adellijketitel.naam != 'Geen titel' and             data.adellijketitel.naam != 'Onbekend' and             data.adellijketitel.naam is not None:
        adellijketitel = getNamedObject(
            frontend.AdellijkeTitel, data.adellijketitel.naam.lower())
    elif data.adelspredikaat: # catch the 'Jonkheer' items
        adellijketitel = getNamedObject(
            frontend.AdellijkeTitel, data.adelspredikaat.lower())
    else:
        adellijketitel = None

    if data.academischetitel and             data.academischetitel.naam != 'Geen' and             data.academischetitel.naam != 'Onbekend' and             data.academischetitel.naam is not None:
        academischetitel = getNamedObject(
            frontend.AcademischeTitel, data.academischetitel.naam.lower()
            )
    else:
        academischetitel = None

    searchable = data.geslachtsnaam
    if data.tussenvoegsel:
        searchable = data.tussenvoegsel+' '+searchable

    persoon = frontend.Persoon(
        adel=bool(data.adel),
        heerlijkheid=heerlijkheden,
        voornaam=data.voornaam,
        tussenvoegsel=data.tussenvoegsel,
        geslachtsnaam=data.geslachtsnaam,
        searchable_geslachtsnaam=searchable,
        geboortedatum=geboortedatum,
        geboortedatum_als_bekend=known_geboortedatum,
        geboorteplaats=data.geboorteplaats or None,
        doopjaar=doopjaar,
        overlijdensdatum=overlijdensdatum,
        overlijdensdatum_als_bekend=known_overlijdensdatum,
        overlijdensplaats=data.overlijdensplaats or None,
        adellijketitel=adellijketitel,
        academischetitel=academischetitel,
        opmerkingen=data.opmerkingen,
        )


# some graph experiments below. keep for reference :-)

# In[1134]:


duplicated = at.loc[~at.duplicated(subset=['AcademischeTitel'])]['AcademischeTitel']


# In[1141]:


dd = at.merge(duplicated, on='AcademischeTitel', indicator=True)


# In[ ]:


dd.duplicated(subset=['AcademischeTitel'])


# In[1106]:


import networkx as nx
G = nx.Graph()


# In[ ]:





# In[1065]:


groups = at.groupby(at.AcademischeTitel)


# In[1118]:


for g in groups:
    G.add_node(g[0])
    for i in g[1]:
        if i not in [g[0], 'index']:
            for n in g[1][i]:
                G.add_node(node_for_adding=n)
                G.add_edge(u_of_edge=g[0],v_of_edge=n)
        
G


# In[1150]:


nx.draw(G, with_labels=True, node_color='blue',
            node_size=40
       )


# list(nx.connected.connected_components(G))

# In[1158]:


d = dict(nx.all_pairs_shortest_path(G))

