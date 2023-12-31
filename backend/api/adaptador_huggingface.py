import time
import pandas as pd
import numpy as np
import re
import requests
import ast
import yaml
import pytz

from scipy import stats
from requests.exceptions import JSONDecodeError
from datetime import datetime

from concurrent.futures import ThreadPoolExecutor
from huggingface_hub import HfApi
from huggingface_hub import ModelCard
from huggingface_hub import hf_hub_url, get_hf_file_metadata

from .models import Model, Entrenament, Metrica, InfoAddicional, ResultatEntrenament, ValorInfoEntrenament, Configuracio


########## PRIMERA PART: EXTRACTION FROM HUGGING FACE

def retrieve_emission_parameters(model):
    """
    Retrieve emission parameters from a given model.

    Args:
        model: The model object.

    Returns:
        A tuple containing emissions, source, training_type, geographical_location, and hardware_used.
    """

    if 'co2_eq_emissions' not in model.cardData:
        return None, None, None, None, None

    if type(model.cardData["co2_eq_emissions"]) is dict:
        emissions_dict = model.cardData["co2_eq_emissions"]
    else:
        emissions = model.cardData["co2_eq_emissions"]
        return emissions, None, None, None, None

    emissions = emissions_dict["emissions"]

    if 'source' in emissions_dict:
        source = emissions_dict['source']
    else:
        source = None

    if 'training_type' in emissions_dict:
        training_type = emissions_dict['training_type']
    else:
        training_type = None

    if 'geographical_location' in emissions_dict:
        geographical_location = emissions_dict['geographical_location']
    else:
        geographical_location = None

    if 'hardware_used' in emissions_dict:
        hardware_used = emissions_dict['hardware_used']
    else:
        hardware_used = None

    return emissions, source, training_type, geographical_location, hardware_used


def find_model_accuracy(modelId):
    """
    Find the accuracy of a model given its ID.

    Args:
        modelId: The ID of the model.

    Returns:
        The accuracy of the model or None if not found.
    """


    try:
        modelCard_text = ModelCard.load(modelId).text
    except:
        return None

    accuracy_regex = r"Accuracy\s*:\s*.*?(?=\n)"


    accuracy_match = re.search(accuracy_regex, modelCard_text)

    if accuracy_match is None:
        return None

    accuracy_match = accuracy_match.group(0)

    accuracy_match = float(accuracy_match.split(':')[1])

    return accuracy_match


def find_model_validation_metric(modelId, metric):
    """
    Find the validation metric of a model given its ID and metric.

    Args:
        modelId: The ID of the model.
        metric: The evaluation metric to search for.

    Returns:
        The validation metric value or None if not found.
    """


    try:
        modelCard_text = ModelCard.load(modelId).text
    except:
        return None

    accuracy_regex = fr'{metric}\s*:\s*.*?(?=\n)'


    accuracy_match = re.search(accuracy_regex, modelCard_text)

    if accuracy_match is None:
        return None

    accuracy_match = accuracy_match.group(0)

    accuracy_match = float(accuracy_match.split(':')[1])

    return accuracy_match

def retrieve_model_tags(model):
    """
    Retrieve tags from a given model.

    Args:
        model: The model object.

    Returns:
        A list of tags associated with the model.
    """

    tags = list(set(model.tags + [model.pipeline_tag]))
    if hasattr(model, 'cardData') and 'tags' in model.cardData:
        if type(model.cardData['tags']) is list:
            try: #we only lose 3 rows by doing this
                tags = list(set(tags + model.cardData['tags']))
            except:
                print(model.cardData['tags'])
        else:
            tags = list(set(tags + [model.cardData['tags']]))

    tags = [tag for tag in tags if tag is not None]


    return tags


def find_model_size(modelId):
    """
    Find the size of a model given its ID.

    Args:
        modelId: The ID of the model.

    Returns:
        The size of the model or None if not found.
    """

    try:
        return get_hf_file_metadata(hf_hub_url(repo_id=modelId, filename="pytorch_model.bin")).size
    except:
        return None


def retrieve_model_datasets(model):
    """
    Retrieve the datasets used by a given model.

    Args:
        model: The model object.

    Returns:
        A list of datasets used by the model.
    """

    if hasattr(model, 'cardData') and 'datasets' in model.cardData:
        if type(model.cardData["datasets"]) is list:
            datasets = model.cardData["datasets"]
        else:
            datasets = model.cardData["datasets"]
    else:
        datasets = ['']

    return datasets


def find_datasets_size(datasets):
    """
    Find the size of datasets used by a given model.

    Args:
        datasets: A list of datasets.

    Returns:
        The total size of the datasets or None if not found.
    """

    datasets_size = 0
    if datasets is None:
        return None

    for dataset in datasets:
        try:
            api = HfApi()
            datasets_size += api.dataset_info(dataset).cardData["dataset_info"]["dataset_size"]
        except:
            pass

    return datasets_size



def extract_from_model_index(model_index):
    """
    Extract evaluation metrics from a model index.

    Args:
        model_index: The model index object.

    Returns:
        A tuple containing accuracy, f1, loss, rouge1, and rougeL.
    """


    accuracy = f1 = loss = rouge1 = rougeL = None
    if model_index is not None and 'results' in model_index and model_index['results'] and  isinstance(model_index['results'][0], dict) \
       and 'metrics' in model_index['results'][0]:
        metrics_list = model_index['results'][0]['metrics']
        for metric_type in metrics_list:

            metric = metric_value = None

            if 'type' in metric_type and 'value' in metric_type:
                if 'value' in metric_type:
                    metric = metric_type['type']
                    metric_value = metric_type['value']

            if metric == 'accuracy':
                accuracy = metric_value
            elif metric_value == 'f1':
                f1 = metric_value
            elif metric_value == 'loss':
                loss = metric_value
            elif metric_value == 'rouge1':
                rouge1 = metric_value
            elif metric_value == 'rougeL':
                rougeL = metric_value

    return accuracy, f1, loss, rouge1, rougeL

def extract_evaluation_from_modelcard(model):
    """
    Extract evaluation metrics from a model card.

    Args:
        model: The model object.

    Returns:
        A tuple containing accuracy, f1, loss, rouge1, and rougeL.
    """


    accuracy = f1 = loss = rouge1 = rougeL = None
    if hasattr(model, 'cardData'):
        if 'model-index' in model.cardData:
            model_index = model.cardData['model-index'][0] if isinstance(model.cardData['model-index'], list) else model.cardData['model-index']
            accuracy, f1, loss, rouge1, rougeL = extract_from_model_index(model_index)
        elif 'model_index' in model.cardData:
            model_index = model.cardData['model_index'][0] if isinstance(model.cardData['model_index'], list) else model.cardData['model_index']
            accuracy, f1, loss, rouge1, rougeL = extract_from_model_index(model_index)

        elif 'metrics' in model.cardData and model.cardData["metrics"] is not None and isinstance(model.cardData["metrics"][0], dict):
            for metric_dict in model.cardData["metrics"]:
                metric, metric_value  = list(metric_dict.items())[0]
                if metric == 'accuracy':
                    accuracy = metric_value
                elif metric_value == 'f1':
                    f1 = metric_value
                elif metric_value == 'loss':
                    loss = metric_value
                elif metric_value == 'rouge1':
                    rouge1 = metric_value
                elif metric_value == 'rougeL':
                    rougeL = metric_value

    return accuracy, f1, loss, rouge1, rougeL


def extract_evaluation_metrics(model, auto):
    """
    Extract evaluation metrics from a model with the option to use auto mode.

    Args:
        model: The model object.
        auto: A boolean flag to indicate if autotrain/autonlp tags should be considered.

    Returns:
        A tuple containing accuracy, f1, loss, rouge1, and rougeL.
    """

    accuracy, f1, loss, rouge1, rougeL = extract_evaluation_from_modelcard(model)

    if auto:
        if accuracy == None:
            accuracy = find_model_validation_metric(model.modelId, 'Accuracy')
        if f1 == None:
            f1 = find_model_validation_metric(model.modelId, r'(F1|Macro F1)')
        if loss == None:
            loss = find_model_validation_metric(model.modelId, 'Loss')
        if rouge1 == None:
            rouge1 = find_model_validation_metric(model.modelId, 'Rouge1')
        if rougeL == None:
            rougeL = find_model_validation_metric(model.modelId, 'RougeL')

    return accuracy, f1, loss, rouge1, rougeL


def api_calls_parameters(model, datasets):

    """
    Get size, datasets size, and creation date from API calls.

    Args:
        model: The model object.
        datasets: A list of datasets.

    Returns:
        A tuple containing size, datasets_size, and created_at.
    """


    size = datasets_size = created_at = None
    api_token = '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'
    headers = {"authorization": f"Bearer {api_token}"}

    try:
        commits = requests.get(f'https://huggingface.co/api/models/{model.modelId}/commits/main', timeout=2, headers=headers)
    except requests.exceptions.Timeout:
        print(f'Timeout error for commits on model {model.modelId}')
        created_at = None
    except JSONDecodeError:
        print(f'JSON decode error for commits on model {model.modelId}')
        created_at = None
    except Exception as e:
        print(f'Unexpected error for commits on model {model.modelId}: {e}')
        created_at = None
    else:
        try:
            created_at = commits.json()[-1]['date']
        except Exception as e:
            print(f'Error extracting "created_at" for model {model.modelId}')
            created_at = None

    return size, datasets_size, created_at


def get_modelcard_text(model):
    """
    Get the text of a model card.

    Args:
        model: The model object.

    Returns:
        The text of the model card or None if not found.
    """


    card_text = None
    try:
        card_text = ModelCard.load(model.modelId).text
    except:
        pass
    return card_text



def process_model(model):
    """
    Process a model and extract relevant information.

    Args:
    model: A tuple containing the model object.

    Returns:
        A dictionary containing the processed model information.
    """

    if model[0] % 10 == 0:
        print(model[0])

    model = model[1]

    try:
        tags = retrieve_model_tags(model)
        datasets = retrieve_model_datasets(model)
        auto = 'autotrain' in tags or 'autonlp' in tags
        library_name = model.library_name if hasattr(model, 'library_name') else None
        accuracy, f1, loss, rouge1, rougeL = extract_evaluation_metrics(model, auto)

        size, datasets_size, created_at = api_calls_parameters(model, datasets)

        card_text = get_modelcard_text(model)
        emissions = source = training_type = geographical_location = hardware_used = None

        if hasattr(model, 'cardData') and "co2_eq_emissions" in model.cardData:
            size = find_model_size(model.modelId)
            datasets_size = find_datasets_size(datasets)
            emissions, source, training_type, geographical_location, hardware_used = retrieve_emission_parameters(model)

        return {'modelId': model.modelId,
                'tags': tags,
                'datasets': datasets,
                'datasets_size': datasets_size,
                'co2_eq_emissions': emissions,
                'source': source,
                'training_type': training_type,
                'geographical_location': geographical_location,
                'hardware_used': hardware_used,
                'accuracy': accuracy,
                'loss': loss,
                'f1': f1,
                'rouge1': rouge1,
                'rougeL': rougeL,
                'size': size,
                'auto': auto,
                'downloads': model.downloads,
                'likes': model.likes,
                'library_name': library_name,
                'lastModified': model.lastModified,
                'created_at': created_at,
                'modelcard_text': card_text}
    except Exception as e:
        print(f'{model.modelId} could not be processed: ', str(e))


def extraction():
    api = HfApi()

    # Retrieve models info through HfApi call
    models = list(api.list_models(
        emissions_thresholds=(0, 10000000000000000000),
        cardData=True,
        full=True,
        fetch_config=True,
        limit=5000,
        sort='last_modified',
        direction=-1,
    ))

    print(len(models))

    models = [(idx, model) for idx, model in enumerate(models)]

    start = time.time()

    # Set the number of threads you want to use for parallel processing
    num_threads = 8 # adjust threads

    # Ens quedem només amb els nous
    cutoff_date = Configuracio.objects.get(id=1).ultimaSincronitzacio
    models_to_process = [(index, model_info) for index, model_info in models if model_info.last_modified >= cutoff_date]
    print("Aquñiiiii")
    print(len(models_to_process))
    print(len(models))

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        models_information = list(executor.map(process_model, models_to_process))


    models_information = [model for model in models_information if model is not None]
    df = pd.DataFrame(models_information)
    end = time.time()
    print(end - start)
    return df


########## SEGONA PART: PREPROCESSING

def split_df(df):
    if len(df) % 2 != 0:  # Handling `df` with `odd` number of rows
        df = df.iloc[:-1, :]
    df1, df2, df3, df4 = np.array_split(df, 4)
    return df1, df2, df3, df4

def select_top_tags(df, n):
    not_tags = [col for col in df.columns if not col.startswith('is_')]
    tags_names = [col for col in df.columns if col.startswith('is_')]
    relevant_tags = df[tags_names].sum(axis=0) > n
    relevant_tags = [index for index, value in zip(relevant_tags.index, relevant_tags.values) if value]
    df = df[not_tags + relevant_tags]
    return df


def one_hot_tags(df):
    df_onehot = df.drop('tags', axis=1).join(
        pd.get_dummies(
            pd.DataFrame(df.tags.tolist(), df.index).stack(),
            prefix='is', prefix_sep='_'
        ).astype(int).groupby(level=0).sum()
    )
    return df_onehot


def enlarge_tag_to_domain_dict(tag, tag_to_domain):
    if 'gpt' in tag or 'bert' in NLP or 'bart' == tag or 't5' == tag:
        tag_to_domain[tag] = 'NLP'
    elif 'bert' in tag:
        tag_to_domain[tag] = 'NLP'

def most_common(lst):
    return max(set(lst), key=lst.count)

def assign_model_domain(tags, tags_to_domain):
    inicial = dict()
    if tags_to_domain['task_to_domain'] is not None:
        inicial.update(tags_to_domain['task_to_domain'])
    if tags_to_domain['model_to_domain'] is not None:
        inicial.update(tags_to_domain['model_to_domain'])
    if tags_to_domain['concepts_to_domain'] is not None:
        inicial.update(tags_to_domain['concepts_to_domain'])
    tags_to_domain = inicial
    model_domains = set()
    tags_domain = set()
    for tag in tags:
        if tag in tags_to_domain:
            model_domains.add(tags_to_domain[tag])
            tags_domain.add(tag)

    if len(model_domains) == 0:
        return None

    if len(model_domains) > 1:
        if 'feature-extraction'in tags_domain:
            if len(model_domains) == 2:
                return 'NLP'
        if 'Multimodal' in model_domains:
            return 'Multimodal'

        return most_common(list(model_domains))

    return model_domains.pop()


def filter_tags(tags, tags_metadata):
    languages_list = tags_metadata['languages']
    return [tag for tag in tags if tag not in languages_list and not tag.startswith(('license:', 'arxiv:', 'dataset:', 'doi:'))]

def tags_treatment(tags, tags_metadata):
    tags = ast.literal_eval(tags) if not isinstance(tags, list) else tags
    tags = filter_tags(tags, tags_metadata)
    tags = ['no-tag'] if not tags else tags
    return [str(tag).lower().replace(' ', '-') for tag in tags]

def set_library(library_name, tags, libraries_list):
    libraries = [tag for tag in tags if tag in libraries_list]
    library_name = list(set(libraries + [library_name])) if not isinstance(library_name, list) else list(set(libraries + library_name))
    return [library for library in library_name if library is not None and not pd.isnull(library)]

def set_language(tags, languages_list):
    languages = [tag for tag in tags if tag in languages_list]
    return list(set(languages))

def set_license(tags, licenses_list):
    licenses = [tag for tag in tags if tag in licenses_list]
    return list(set(licenses))

def concat_dataset_splits(df1,df2,df3,df4):
    all_columns = set(df1.columns).union(df2.columns).union(df3.columns).union(df4.columns)

    # Concatenate the DataFrames vertically with an outer join
    df = pd.concat([df1, df2, df3, df4], axis=0, join='outer', ignore_index=True)

    # Find the non-shared columns
    dfs = [df1, df2, df3, df4]
    non_shared_columns = set()

    for i, df1 in enumerate(dfs):
        for df2 in dfs[i + 1:]:
            non_shared_columns = non_shared_columns.union(set(df1.columns).symmetric_difference(df2.columns))

    # Fill NaN values with zeros only for non-shared columns
    for col in non_shared_columns:
        df[col] = df[col].fillna(0)

    return df

def normalize_performance_metric(metric, metric_name):
    if isinstance(metric, float):
        if metric_name in ['f1', 'accuracy']:
            if float(metric) > 1:
                return float(metric)/100
        return float(metric)

    if metric is None or pd.isnull(metric) or '[' in metric:
        return None

    if '%' in metric:
        metric = float(metric.replace('%', ''))
    elif ',' in metric:
        metric = float(metric.replace(',', '.'))
    elif isinstance(ast.literal_eval(metric), dict):
        metric = float(ast.literal_eval(metric)[metric_name])

    if metric_name in ['f1', 'accuracy']:
        if float(metric) > 1:
            return float(metric)/100
    if float(metric) > 1:
        print(metric, metric_name)
    return float(metric)


def extract_context_info(text):
    patterns = {
        'hardware_type': r'[-*]*\s*(?:hardware|Hardware)(?:\s*[Tt]ype)*\s*[:]+\s*(.+)',
        'hours_used': r'[-*]*\s*Hours used\s*[:]+\s*(.+)',
        'cloud_provider': r'[-*]*\s*[Cc]loud [Pp]rovider\s*[:]+\s*(.+)',
        'compute_region': r'[-*]*\s*[Cc]ompute [Rr]egion\s*[:]+\s*(.+)',
        'carbon_emitted': r'[-*]*\s*[Cc]arbon [Ee]mitted\s*[:]+\s*(.+)',
        'training_type': r'[-*]*\s*(?:training|Training)(?:\s*[Tt]ype)*\s*[:]+\s*(.+)',

    }

    if text is None or pd.isnull(text):
        return {'hardware_type':None, 'hours_used':None, 'cloud_provider':None, 'compute_region':None, 'carbon_emitted':None, 'training_type':None}


    results = {}
    for key, pattern in patterns.items():
        regex = re.compile(pattern, re.IGNORECASE)
        match = regex.search(text)
        results[key] = match.group(1) if match else None

    return results

def context_metrics_treatment(df):
    if 'modelcard_text' in df:
        context_info_results = [extract_context_info(text) for text in df['modelcard_text']]


        null_phrases = ['Unknown', 'unknown', 'needed', 'Needed']
        df['hardware_used'] = [context_info_results[idx]['hardware_type']
                               if pd.isnull(x) and all([phrase not in str(context_info_results[idx]['hardware_type']) for phrase in null_phrases]) else x
                               for idx, x in enumerate(df['hardware_used'])]
        df['geographical_location'] = [context_info_results[idx]['compute_region']
                                       if pd.isnull(x) and all([phrase not in str(context_info_results[idx]['compute_region']) for phrase in null_phrases]) else x
                                       for idx, x in enumerate(df['geographical_location'])]
        df['co2_eq_emissions'] = [context_info_results[idx]['carbon_emitted']
                                  if pd.isnull(x) and all([phrase not in str(context_info_results[idx]['carbon_emitted']) for phrase in null_phrases]) else x
                                  for idx, x in enumerate(df['co2_eq_emissions'])]
        df['hours_used'] = [context_dict['hours_used'] for context_dict in context_info_results]
        df['cloud_provider'] = [context_dict['cloud_provider'] for context_dict in context_info_results]

    return df

def performance_metrics_treatment(df):
    df['f1'] = df['f1'].apply(lambda x: normalize_performance_metric(x, 'f1')) if 'f1' in df.keys() else None
    df['accuracy'] = df['accuracy'].apply(lambda x: normalize_performance_metric(x, 'accuracy')) if 'accuracy' in df.keys() else None
    df['rouge1'] = df['rouge1'].apply(lambda x: normalize_performance_metric(x, 'rouge1')) if 'rouge1' in df.keys() else None
    df['rougeL'] = df['rougeL'].apply(lambda x: normalize_performance_metric(x, 'rougeL')) if 'rougeL' in df.keys() else None
    return df


def harmonize_co2(co2):

    if isinstance(co2, float):
        return co2

    if pd.isnull(co2):
        return None
    co2_found = re.match(r'\d+\.\d+|\d+', co2)

    if co2_found is None:
        return None

    return float(co2_found.group(0))


def min_max_normalize(series):
    return (series - series.min()) / (series.max() - series.min())

def performance_score(df):
    metrics = ['accuracy', 'f1', 'rouge1', 'rougeL']

    df['f1'] = min_max_normalize(df['f1'])
    df['accuracy'] = min_max_normalize(df['accuracy'])
    df['rouge1'] = min_max_normalize(df['rouge1'])
    df['rougeL'] = min_max_normalize(df['rougeL'])
    return df.apply(lambda row: stats.hmean([row[metric] for metric in metrics if not np.isnan(row[metric])]), axis=1)


def preprocessing_rawData(df):
    pd.options.mode.chained_assignment = None

    with open('./api/tags_metadata.yaml') as file:
        tags_metadata = yaml.safe_load(file)


    df = performance_metrics_treatment(df)
    df = context_metrics_treatment(df)

    #Curation
    df['modelName'] = df['modelId'].apply(lambda x: x.split('/')[1] if len(x.split('/')) > 1 else x) #remove author from modelId
    df['modelAuthor'] = df['modelId'].apply(lambda x: x.split('/')[0] if len(x.split('/')) > 1 else None) #remove name from modelId
    df['co2_eq_emissions'] = df['co2_eq_emissions'].apply(lambda co2: harmonize_co2(co2)) #harmonize plenty of co2 values
    df['tags'] = df['tags'].apply(lambda tags: tags_treatment(tags, tags_metadata)) # filter and treat tags
    df['lastModified'] = pd.to_datetime(df['lastModified']) # convert the 'lastModified' column to datetime objects
    df['created_at'] = pd.to_datetime(df['created_at']) # convert the 'lastModified' column to datetime objects
    df['library_name'] = df.apply(lambda row: set_library(row['library_name'], row['tags'], tags_metadata['libraries']), axis=1) # adds libraries used by model
    df["datasets_size"] = df["datasets_size"].replace(0, np.nan)
    df = df[df['co2_eq_emissions'] != 0]


    #Feature Engineering
    df['co2_reported'] = df['co2_eq_emissions'].apply(lambda x: 0 if pd.isnull(x) or x is None else 1)
    df['license'] = df['tags'].apply(lambda tags: set_license(tags, tags_metadata['licenses']))
    df['language'] = df['tags'].apply(lambda tags: set_language(tags, tags_metadata['languages']))
    df['domain'] = df['tags'].apply(lambda tags: assign_model_domain(tags, tags_metadata['tags_to_domain']))
    df['year_month'] = df['created_at'].apply(lambda x: x.strftime('%Y-%m')) #  column 'year_month' to group the data monthly
    df['size_efficency'] = df['size'] / df['co2_eq_emissions']
    df['performance_score'] = performance_score(df)

    # we split, one hot and then combine splits to avoid memory overflow if we one-hot'ed with the whole dataset alltogether
    df1,df2,df3,df4 = split_df(df)
    df1,df2,df3,df4 = one_hot_tags(df1), one_hot_tags(df2), one_hot_tags(df3), one_hot_tags(df4)
    df1,df2,df3,df4 = select_top_tags(df1, 100), select_top_tags(df2, 100), select_top_tags(df3, 100), select_top_tags(df4, 100)
    df = concat_dataset_splits(df1,df2,df3,df4)

    return df

"""## Preprocessing of CO2 data

We join the co2 subset from the raw preprocessed data with the cleaned dataset and continue the preprocessing on the co2.
"""

def read_df_processed(df):
    # df = df.drop(['Unnamed: 0.1', 'Unnamed: 0'], axis=1)
    df['library_name'] = df['library_name'].apply(lambda libraries:  ast.literal_eval(libraries) if not isinstance(libraries, list) else libraries)
    df['datasets'] = df['datasets'].apply(lambda datasets: [''] if any(pd.isnull(element) for element in datasets) else [datasets] if '[' not in datasets else ast.literal_eval(datasets))

    return df


def read_df_clean():
    df = pd.read_csv('./HFClean.csv')
    df = df.drop(['Unnamed: 0'], axis=1)
    df['library_name'] = df['library_name'].apply(lambda libraries:  ast.literal_eval(libraries) if not isinstance(libraries, list) else libraries)
    df['datasets'] = df['datasets'].apply(lambda datasets: [''] if pd.isnull(datasets) else [datasets] if '[' not in datasets else ast.literal_eval(datasets))

    return df


def merge_dataFrames(df, df_clean):
    df1 = df
    df2 = df_clean

    # Merge the dataframes
    merged = df1.merge(df2, on='modelName', how='left', suffixes=('', '_y'))

    # Replace _x columns with _y columns (from HFClean.csv) when _y is not null
    for column in merged.columns:
        if '_y' in column:
            merged[column.replace('_y', '')] = merged[column].where(merged[column].notnull(), merged[column.replace('_y', '')])

    # Drop _y columns
    df = merged[df1.columns]

    return df


def combine_sources(source, auto):

    if auto:
        return 'AutoTrain'
    if source == 'code carbon':
        return 'Code Carbon'
    if 'mlco2' in source or 'ML CO2' in source:
        return 'MLCO2'
    if 'BLOOM' in source:
        return 'Article'
    if 'Google Cloud' in source:
        return 'Google Cloud Footprint'

    return 'Not Specified'

def combine_location(location):

    if 'East US' in location:
        return 'East US'
    if location == 'Frankfurt an Main, Germany (500-600 gCO2eq/kWh)':
        return 'Frankfurt an Main, Germany'
    return location


def combine_training_type(training_type):

    if 'fine' in training_type:
        return 'fine-tuning'
    if 'pre' in training_type:
        return 'pretraining'

    return 'Not Specified'

def create_performance_metrics(row):
    return {'accuracy': row['accuracy'], 'f1': row['f1'], 'rouge1': row['rouge1'], 'rougeL': row['rougeL']}


def preprocessing_co2(df):
    df = read_df_processed(df)

    # df_clean = read_df_clean()

    df = df[df['co2_reported'] == True]

    wanted_columns = [col for col in df.columns if not col.startswith('is_')]
    df = df[wanted_columns]

    # df = merge_dataFrames(df, df_clean)

    df['domain'] = df['domain'].fillna('Not Specified')
    df['training_type'] = df['training_type'].fillna('Not Specified')
    df['source'] = df['source'].fillna('Not Specified')
    df['geographical_location'] = df['geographical_location'].fillna('Not Specified')
    df['hardware_used'] = df['hardware_used'].fillna('Not Specified')

    df['source'] = df.apply(lambda row: combine_sources(row['source'], row['auto']), axis=1)
    df['geographical_location'] = df['geographical_location'].apply(lambda location: combine_location(location))
    df['training_type'] = df['training_type'].apply(lambda training_type: combine_training_type(training_type))
    df['size_efficency'] = df['size'] / df['co2_eq_emissions']
    df['datasets_size_efficency'] = df['datasets_size'] / df['co2_eq_emissions']
    df['downloads'] = df['downloads'].astype(int)
    df['likes'] = df['likes'].astype(int)
    df['co2_reported'] = df['co2_reported'].astype(int)

    df['created_at'] = pd.to_datetime(df['created_at'])
    df['created_at'] = df['created_at'].dt.date

    df['lastModified'] = pd.to_datetime(df['lastModified'])
    df['lastModified'] = df['lastModified'].dt.date
    df['performance_metrics'] = df.apply(create_performance_metrics, axis=1)

    df = df.rename(columns={'hardware_used': 'environment'})
    wanted_columns = ['modelName', 'modelAuthor', 'datasets', 'datasets_size', 'co2_eq_emissions', 'co2_reported', 'source', 'training_type', 'geographical_location', 'environment', 'performance_metrics', 'performance_score',
                      'downloads', 'likes', 'library_name', 'domain', 'size', 'created_at', 'lastModified', 'size_efficency', 'datasets_size_efficency']
    df = df[wanted_columns]

    return df



########## TERCERA PART: UPDATE / INSERT BD
def replace_none(obj):
    # Posar None, nan i Not Specified com a None
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = replace_none(value)
        return obj
    elif isinstance(obj, list):
        return [replace_none(item) for item in obj]
    elif pd.isna(obj) or obj == 'nan' or obj == 'Not Specified':
        return None
    else:
        return obj


def inicialitzar_entrenament(entrenament, model_info):
    metriques = Metrica.objects.filter(fase='T')
    for metrica in metriques:
        ResultatEntrenament.objects.create(
            entrenament=entrenament,
            metrica=metrica,
            valor=model_info[metrica.id]
        )

    informacions = InfoAddicional.objects.filter(fase='T')
    for informacio in informacions:
        if informacio.id in model_info.keys() and model_info[informacio.id]:
            ValorInfoEntrenament.objects.create(
                entrenament=entrenament,
                infoAddicional=informacio,
                valor=model_info[informacio.id]
            )


def crear_model(model_info):
    model = Model.objects.create(
        nom=model_info['modelName'],
        autor=model_info['modelAuthor'],
    )

    entrenament = Entrenament.objects.create(
        model=model,
    )

    if 'created_at' in model_info.keys() and model_info['created_at']:
        dataCreacio = datetime.strptime(model_info['created_at'].strftime('%Y-%m-%d'), '%Y-%m-%d')
        model.dataCreacio = dataCreacio
        model.save()
        entrenament.dataRegistre = dataCreacio
        entrenament.save()

    inicialitzar_entrenament(entrenament, model_info)


def actualitzar_model(model, model_info):
    # Si tenim data de creació i trobem un entrenament amb aquella data, actualitzarem les dades de l'entrenament.
    dataCreacio = None
    if 'created_at' in model_info.keys() and model_info['created_at']:
        dataCreacio = datetime.strptime(model_info['created_at'].strftime('%Y-%m-%d'), '%Y-%m-%d')

    try:
        entrenament = Entrenament.objects.get(model=model, dataRegistre=dataCreacio)
        metriques = Metrica.objects.filter(fase='T')
        for metrica in metriques:
            # Fem get_or_create per si hi ha noves mètriques
            resultat, created = ResultatEntrenament.objects.get_or_create(entrenament=entrenament, metrica=metrica)
            resultat.valor = model_info[metrica.id]
            resultat.save()

        informacions = InfoAddicional.objects.filter(fase='T')
        for informacio in informacions:
            if informacio.id in model_info.keys() and model_info[informacio.id]:
                info, created = ValorInfoEntrenament.objects.get_or_create(entrenament=entrenament, infoAddicional=informacio)
                info.valor = model_info[informacio.id]
                info.save()

    # En cas que no hi hagi data o no coincideixi amb cap entrenament del model, en crearem un de nou.
    except Entrenament.DoesNotExist:
        entrenament = Entrenament.objects.create(
            model=model,
        )
        if dataCreacio:
            entrenament.dataRegistre = dataCreacio
            entrenament.save()
        inicialitzar_entrenament(entrenament, model_info)


def modify_database(df):
    created = []
    updated = []
    for model_json in df:
        try:
            model = Model.objects.get(nom=model_json['modelName'], autor=model_json['modelAuthor'])
            actualitzar_model(model, model_json)
            updated.append(model_json['modelName'])
            print('[SINCRO HF] ' + model_json['modelName'] + ' updated')
        except Model.DoesNotExist:
            crear_model(model_json)
            created.append(model_json['modelName'])
            print('[SINCRO HF] ' + model_json['modelName'] + ' created')
    return created, updated


########## MAIN
def sincro_huggingFace():
    try:
        created = []
        updated = []

        df_extracted = extraction()
        print('[SINCRO HF] extraction done')
        if len(df_extracted) == 0:
            print('[SINCRO HF] no models to process')
        else:
            df_preprocessed_raw = preprocessing_rawData(df_extracted)
            print('[SINCRO HF] pre raw done')
            df_final = preprocessing_co2(df_preprocessed_raw)
            print('[SINCRO HF] pre co2 done')
            df_final.to_csv('./hf_sincro.csv', index=False)

            # ToDo: Delete després de fer proves!!!
            #df_final = pd.read_csv('./hf_sincro.csv')

            df_json_records = df_final.to_json(orient='records')
            json_list = pd.read_json(df_json_records, orient='records').to_dict(orient='records')
            json_list_replaced = replace_none(json_list)

            created, updated = modify_database(json_list_replaced)

        configuracio = Configuracio.objects.get(id=1)
        configuracio.ultimaSincronitzacio = datetime.now(pytz.timezone('Europe/Madrid'))
        print(configuracio)
        print(configuracio.ultimaSincronitzacio)
        configuracio.save()

        return created, updated
    except Exception as e:
        print('[SINCRO HF] ' + str(e))
        return 'KO', 'KO'
