import os
import yaml
from pathlib import Path
from gpt_box import GPT_Box


class Slide_box:
    def __init__(self) -> None:
        self.slides_folder_path: str = "./ScrapedSlideJson"
        self.slides_folder_path: str = Path(self.slides_folder_path).resolve()

        self.full_slide_paths: list[str] = []

        for root, _, files in os.walk(self.slides_folder_path):
            for file in files:
                if file.endswith(".json"):
                    self.full_slide_paths.append(os.path.join(root, file))


class Cluster_Generator:
    def __init__(self) -> None:
        self.slide_box: Slide_box = Slide_box()

        self.template_path: str = "./templates"
        self.template_path: str = Path(self.template_path).resolve()

        self.cluster_yml_path = self.template_path / "cluster.yml"
        self.template_str = self.cluster_yml_path.read_text()

        self.cluster_folder_path: str = "./Generated_Clusters"
        self.cluster_folder_path: str = Path(
            self.cluster_folder_path).resolve()

        self.gpt_box = GPT_Box()

        self.prompt = """
            You are a helpful assistant. You will be given a json that contains the entire lecture slides. In the format of: [slide_number: slide_info].
            The json might contain multiple topics such as arrays and dictionaries but they also might just contain one topic. 

            Your task is to cluster the slides into topics. You can use the slide number and the slide info to help you cluster the slides.

            The following template is provided to you to help you with the clustering. The template is in yaml format.


            Cluster1: 
                Main_Topic: 
                    - Topic
                Nodes:
                    - Concept1
                    - Concept2

            Cluster2:
                Main_Topic:
                    - Topic
                Nodes:
                    - Concept1
                    - Concept2
                    - Concept3

            ...
            
            For example, if the json contains topics of dictionaries and arrays, you can cluster the slides into two topics: dictionaries and arrays along with the relevant subtopics. DO NOT INCLUDE THE SLIDE NUMBER. Do not create more than 5 subtopics / nodes for each topic.
            Each subtopic should represent ONE SINGLE IDEA. 
            
            DO NOT GIVE ME SUBTOPICS LIKE THIS: "List Operations (append, sort, reverse)" or "indices and ordering".
            
            INSTEAD GIVE ME: append, sort, reverse, indices, ordering. Each as its own subtopic.

            And try to be as specific as you can. For example, if the slide is about "looping through dictionaries", you can say "looping through dictionaries" as a subtopic. 

            As an example of what you can return, the following is an example of a cluster.yml file:

            Cluster1: 
            Main_Topic: 
                - Dictionaries
            Nodes:
                - looping through dictionaries
                - creating dictionaries
                ...

            Don't say anything like "Hello!" or "Certainly". I just want the YAML. Here is the given json:
        """

    def generate_clusters(self) -> None:
        pass

    def generate_one_cluster(self, slide_path: str) -> None:
        """
        Generate one cluster for a given slide json file.

        Args:
            slide_path: str: The path to the slide json file.

        Returns:
            None

        """
        slide_json_text: str = Path(slide_path).read_text(encoding='utf-8')
        entire_prompt: str = self.prompt + slide_json_text

        print("Sending message to GPT-4o model...")
        response = self.gpt_box.send_message(entire_prompt)

        removed_delimiters = response.replace("```yaml", "").replace("```", "")

        print(removed_delimiters)
        self.write_cluster_response_to_file(
            removed_delimiters, Path(slide_path).name.replace(".json", ".yml"))

    def write_cluster_response_to_file(self, generated_response: str, file_name: str) -> None:
        """
        Write the generated response to a file.

        Args:
            generated_response: str: The generated response.
            file_name: str: The name of the file to write the response to.

        Returns:
            None

        """
        file_path = self.cluster_folder_path / file_name
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(generated_response)

        print(f"Response written to {file_path}.")


if __name__ == "__main__":
    test = Cluster_Generator()
    test.generate_one_cluster(test.slide_box.full_slide_paths[0])
