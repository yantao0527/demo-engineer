from pathlib import Path

class File:
    def __init__(self, filename, path=None, content=None, is_dir=False):
        self.filename: str = filename
        self.is_dir: bool = is_dir
        self.path: Path = path
        self.content: str = content
        self.dirty: bool = False

    def load(self):
        if not self.path: return
        full = self.path / self.filename
        with full.open("r", encoding="utf-8") as f:
            self.content = f.read()
        self.dirty = False

    def save(self):
        if not self.path: return
        if not self.content: return
        if not self.dirty: return
        full = self.path / self.filename
        full.write_text(self.content, encoding="utf-8")
        self.dirty = False

    def update(self, content):
        self.content = content
        self.dirty = True

class Dir(File):
    def __init__(self, path: Path):
        super().__init__(path.name, path, None, True)
        self.files = []

    def load(self):
        for x in self.path.iterdir():
            if x.is_dir():
                dir = Dir(x)
                self.files.append(dir)
                dir.load()
            elif x.is_file():
                file = File(x.name, self.path)
                self.files.append(file)
                file.load()

    def save(self):
        self.path.mkdir(parents=True, exist_ok=True)
        for x in self.files:
            x.save()

    def add_file(self, filename, content):
        file = File(filename, self.path, content)
        file.dirty = True
        self.files.append(file)

    def get_file(self, filename):
        for x in self.files:
            if x.filename == filename:
                return x
        return None

    def add_dir(self, dirname):
        dir = Dir(self.path / dirname)
        self.files.append(dir)
        return dir
    
    def get_dir(self, dirname):
        for x in self.files:
            if x.filename == dirname:
                return x
        return self.add_dir(dirname)

AI_PROMPT = "ai_prompt.txt"
AI_LOG = "ai_log"
SRC_DIR = "src"

class Project:
    def __init__(self, root):
        self.root = root
        path = Path(root).absolute()
        self.root_dir = Dir(path)
        self.name = path.name
        self.src_dir: Dir = self.root_dir.get_dir(SRC_DIR)

    def load_all_file(self):
        self.root_dir.load()

    def save_all_file(self):
        self.root_dir.save()
        
    def get_ai_prompt(self):
        file = self.root_dir.get_file(AI_PROMPT)
        if file:
            return file.content
        else:
            return ""
        
    def set_ai_prompt(self, prompt_text):
        file = self.root_dir.get_file(AI_PROMPT)
        if file:
            file.update(prompt_text)
        else:
            self.root_dir.add_file(AI_PROMPT, prompt_text)

    def set_src_file(self, filename, content):
        file = self.src_dir.get_file(filename)
        if file:
            file.update(content)
        else:
            self.src_dir.add_file(filename, content)
        