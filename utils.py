import pandas as pd

def create_dataframe_sankey(data, value_column, *columns, **filtros):
    for col in columns:
        if col not in data.columns:
            raise ValueError
    
    groupbys = []
    for idx, col in enumerate(columns[:-1]):
        i = data.groupby([columns[idx], columns[idx + 1]])[value_column].sum().reset_index()
        i.columns = ['source', 'target', 'value']
        groupbys.append(i)

    conc = pd.concat(groupbys, ignore_index=True)

    for key, values in filtros.items():
        for value in values:
            conc = conc[conc[key] != value]

    info = enumerate(list(set(conc['source'].unique().tolist() + conc['target'].unique().tolist())))

    dic_info = dict(info)

    rev_info = {}
    for key, value in dic_info.items():
        rev_info[value] = key

    conc['source'] = conc['source'].map(rev_info)
    conc['target'] = conc['target'].map(rev_info)



    return rev_info, conc

def create_dataframe_sankey2(data, value_column, *columns, **filtros):
    for col in columns:
        if col not in data.columns:
            raise ValueError

    
    groups = {idx: data[column].unique().tolist() for idx, column in enumerate(columns)}
    groupbys = []

    nodes_list = []
    pos_list = []
    
    colors_nodes = dict(enumerate(["#2F399B", "#F7B261", "#0FB7B3", "#81D3CD"]))
    for idx, column in enumerate(columns):
        for i, value in enumerate(data[column].unique()):
            if str(idx) in filtros.keys():
                if value in filtros[str(idx)]:
                    continue           
            nodes_list.append(value)
            pos_list.append(idx)


    nodes = pd.DataFrame({'names':nodes_list,
                  'pos':pos_list}).reset_index().rename(columns={'index':'id'})
    nodes['x_pos'] = (nodes['pos'] / (len(columns) - 1)) + 0.02
    nodes['x_pos'] = [0.96 if v >=1 else v for v in nodes['x_pos']]
    nodes['color'] = nodes['pos'].map(colors_nodes)

    colors_links = dict(enumerate(["#D9D9ED", "#FFE9C5", "#CBECEF"]))

    for idx, col in enumerate(columns[:-1]):
        i = (data
             .groupby([columns[idx], columns[idx + 1]])[value_column]
             .sum()
             .reset_index())
        
        
        i.columns = ['source', 'target', 'value']
        i = i[~i['source'].isin(list(filtros.values())[0])]
        
        i['color'] = colors_links[idx]
        groupbys.append(i)

    conc = pd.concat(groupbys, ignore_index=True)

    dict_info = dict(nodes[[ 'names', 'id']].values)

    conc['source'] = conc['source'].map(dict_info)
    conc['target'] = conc['target'].map(dict_info)
    

    return nodes, dict_info, conc