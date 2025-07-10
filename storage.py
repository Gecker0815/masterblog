import json
import copy

class Storage:

    def __init__(self):
        self.posts = self.load()

    def load(self):
        try:
            with open("data.json", "r", encoding="utf-8") as fileobj:
                return json.load(fileobj)
        except (FileNotFoundError, json.JSONDecodeError):
            print("File not found or unreadable. Starting with empty post list.")
            return []

    def save(self):
        with open("data.json", "w", encoding="utf-8") as fileobj:
            json.dump(self.posts, fileobj, ensure_ascii=False, indent=4)

    def list_posts(self):
        return copy.deepcopy(self.posts)

    def generate_unique_id(self):
        if not self.posts:
            return 1
        return max(post.get("id", 0) for post in self.posts) + 1

    def add(self, post):
        required_fields = ["author", "title", "content"]
        for field in required_fields:
            if field not in post or not isinstance(post[field], str):
                raise ValueError(f"Invalid or missing field: {field}")
        if "id" in post:
            raise ValueError("Post should not include 'id'; it is auto-assigned.")

        post["id"] = self.generate_unique_id()
        post["likes"] = 0
        self.posts.append(post)
        self.save()
        print(f"Added post with ID {post['id']}")

    def read(self, post_id):
        if not isinstance(post_id, int):
            raise TypeError("ID must be an integer.")

        for post in self.posts:
            if post.get("id") == post_id:
                return copy.deepcopy(post)

        raise ValueError(f"No post found with ID {post_id}")

    def like(self, post_id, like=None):
        if not isinstance(post_id, int):
            raise TypeError("ID must be an integer.")

        for post in self.posts:
            if post.get("id") == post_id:
                if like is not None:
                    if not isinstance(like, int):
                        raise TypeError("Like must be an integer.")
                    post["likes"] = post.get("likes", 0) + 1

                self.save()
                print(f"Post with ID {post_id} has been updated.")
                return

        raise ValueError(f"No post found with ID {post_id}")

    def update(self, post_id, title=None, content=None, like=None):
        if not isinstance(post_id, int):
            raise TypeError("ID must be an integer.")

        if title is None and content is None:
            raise ValueError("At least one of title or content must be provided.")

        for post in self.posts:
            if post.get("id") == post_id:
                if title is not None:
                    if not isinstance(title, str):
                        raise TypeError("Title must be a string.")
                    post["title"] = title

                if content is not None:
                    if not isinstance(content, str):
                        raise TypeError("Content must be a string.")
                    post["content"] = content

                if like is not None:
                    if not isinstance(like, int):
                        raise TypeError("Like must be an integer.")
                    post["likes"] += like

                self.save()
                print(f"Post with ID {post_id} has been updated.")
                return

        raise ValueError(f"No post found with ID {post_id}")

    def delete(self, post_id):
        if not isinstance(post_id, int):
            raise TypeError("ID must be an integer.")

        original_count = len(self.posts)
        self.posts = [post for post in self.posts if post.get("id") != post_id]

        if len(self.posts) < original_count:
            self.save()
            print(f"Post with ID {post_id} has been deleted.")
        else:
            raise ValueError(f"No post found with ID {post_id}")
