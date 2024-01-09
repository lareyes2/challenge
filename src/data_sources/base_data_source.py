import pandas as pd
from abc import ABC, abstractmethod


class BaseDataSource(ABC):
    @abstractmethod
    def read(self) -> pd.DataFrame:
        pass
