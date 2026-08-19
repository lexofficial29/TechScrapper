# TechScrapper

TechScrapper is scanning tool designed for gathering information about the technologies used for creating certain websites.

## How to install

1. Donwload the repo

```git clone https://github.com/lexofficial29/TechScrapper.git```

Enter the  folder
```cd TechScrapper```

2. Create the environment and load it

```python3 -m venv ./venv```

```source venv/bin/activate```

3. Install the dependencies

```pip install -r requirements.txt ```

4. Install Playwright deps

```playwright install```

5. Modify dataframe with your desired parquet file in main.py

```df = pd.read_parquet('data/example1.parquet')``` <--- modify here or leave as is for testing

6. Run the project

```python3 main.py```

## Output

Output will be saved automatically in output/output.json

## Results

![Results image](https://i.imgur.com/bUshkjh.png)
