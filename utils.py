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