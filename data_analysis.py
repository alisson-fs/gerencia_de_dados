import pandas as pd
import matplotlib.pyplot as plt
import json


def convert_jsonl_to_dataframe(path: str) -> None:
    data = []
    with open(path, "r") as file:
        for line in file:
            data.append(json.loads(line))
    return pd.DataFrame(data)


def generate_free_shipping_pie_chart(path: str) -> None:
    df = convert_jsonl_to_dataframe(path)
    count_free_shipping = df["free_shipping"].value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(
        count_free_shipping,
        labels=count_free_shipping.index,
        autopct="%1.1f%%",
        startangle=90,
    )
    plt.title("Frete Grátis")
    plt.show()


def generate_reviews_rating_bar_chart(path: str) -> None:
    df = convert_jsonl_to_dataframe(path)
    count_reviews_rating = (
        df["reviews_rating"]
        .str.replace("estrelas", "")
        .str.replace(" de 5", "")
        .value_counts()
        .sort_index()
    )

    plt.figure(figsize=(10, 6))
    count_reviews_rating.plot(kind="bar")
    plt.xlabel("Nota de Avaliação")
    plt.ylabel("Quantidade")
    plt.title("Distribuição das Notas de Avaliação")
    plt.show()


def format_num_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    df[column] = (
        df[column]
        .str.replace("(", "")
        .str.replace(")", "")
        .str.replace(".", "")
        .astype(float)
    )
    return df


def get_column_mean(path: str, column: str) -> float:
    df = convert_jsonl_to_dataframe(path)
    df = format_num_column(df, column)
    return df[column].fillna(0).mean()


meli_file = "data/meli.jsonl"
generate_free_shipping_pie_chart(meli_file)
generate_reviews_rating_bar_chart(meli_file)
print(get_column_mean(meli_file, "price"))
print(get_column_mean(meli_file, "reviews_amount"))

amazon_file = "data/amazon.jsonl"
generate_free_shipping_pie_chart(amazon_file)
generate_reviews_rating_bar_chart(amazon_file)
print(get_column_mean(amazon_file, "price"))
print(get_column_mean(amazon_file, "reviews_amount"))
