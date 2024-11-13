import yaml
from pathlib import Path
import re


class YAML_Parser:
    def __init__(self):
        self.folder_path = Path("Generated_Clusters")
        self.output_file_path = Path("all_concepts.yml")

    def clean_column_name(self, column_name: str) -> str:
        """
        Clean the column name to remove special characters and spaces.
        """
        # Replace invalid characters with underscores
        cleaned_name = re.sub(r"[^a-zA-Z0-9_]", "_", column_name)

        # Ensure the name starts with a letter or underscore
        if not re.match(r"^[a-zA-Z_]", cleaned_name):
            cleaned_name = "_" + cleaned_name

        # Truncate to 63 characters
        return cleaned_name[:63].lower()

    def parse_all_clusters(self) -> None:
        """
        Parse all the cluster files in the folder and write them to a single YAML file.
        """
        all_clusters = set()
        for file_path in self.folder_path.iterdir():
            if file_path.is_file():
                with open(file_path, "r", encoding="utf-8") as file:
                    cluster = yaml.safe_load(file)
                    counter = 1
                    start = f"Cluster{counter}"

                    curr = []

                    while start in cluster:
                        curr += cluster[start]["Nodes"]
                        counter += 1
                        start = f"Cluster{counter}"

                    all_clusters |= set(curr)

        res = set()

        for name in all_clusters:
            res.add(self.clean_column_name(name))

        res = list(res)
        with open(self.output_file_path, "w", encoding="utf-8") as file:
            yaml.dump(res, file)

        print(f"Clusters written to {self.output_file_path}.")


if __name__ == "__main__":
    parser = YAML_Parser()
    parser.parse_all_clusters()
