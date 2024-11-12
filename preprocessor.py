import pandas as pd


def preprocess(bios, results, final2024):
    
    # merging 
    df = pd.merge(bios,results, how='outer', on=['athlete_id'])

    df = df[~df['Year'].isin([2010, 2014, 2018])]


    # concatinating the data of 2024 olympics 
    final2024.columns = final2024.columns.str.strip()

    final2024['Bronze'] = final2024['Bronze'].astype('object')
    final2024['Gold'] = final2024['Gold'].astype('object')
    final2024['Silver'] = final2024['Silver'].astype('object')

    df = pd.concat([df, final2024], ignore_index=True)


    # filtering for summer olympics
    df = df[df['Type'] == 'Summer']


    # dropping duplicates
    df.drop_duplicates(inplace=True)

    return df