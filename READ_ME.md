## Proposed Algorithm

### Citation:
Please give references for using the algorithms in:

**Disjoint Community Detection:**

Çetin, P. ve Emrah Amrahov, Ş. 2022. A new network-based community detection algorithm for disjoint communities. Turkish Journal of Electrical Engineering & Computer Sciences, doi: 10.3906/elk-2109-52

**Overlapping Community Detection:**

Çetin, P. ve Emrah Amrahov, Ş. 2022. A new overlapping community detection algorithm based on similarity of neighbors in complex networks. Kybernetika, 58 (2), 277-300. doi: 10.14736/kyb-2022-2-0277

## Generating LFR Datasets

It is recommended to produce data with LFR-Benchmark and then use it within the code by `convert_generated_files_into_my_format` function inside the `dataset_generator`.

## Installation of Virtual Environment

If you want to use a virtual environment, you can create and activate it as follows:

**Create a virtual environment:**
```sh
python -m venv venv
```

**Activate the virtual environment:**
```sh
Windows:
venv\Scripts\activate
macOS/Linux:
source venv/bin/activate
```

**Install required packages in requirements.txt file:**
```sh
pip install -r requirements.txt
```

**Run Project:**
```sh
python main.py
```