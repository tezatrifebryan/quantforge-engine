from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class LoggingConfig:
    level:str="INFO"
    file_name:str="engine.log"
