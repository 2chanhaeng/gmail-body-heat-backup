import pandas as pd
from pathlib import Path

__all__ = ["save_csv"]

DB_PATH = Path(".")


def groupby(date_name_temp):
    ym_dt_nm_index = date_name_temp.groupby(by=["YM", "DT", "Name"], group_keys=True)[
        ["Temp"]
    ].apply(pd.DataFrame)
    ym_dt_nm_index.index = ym_dt_nm_index.index.droplevel(3)
    ym_dt_index_name_col = ym_dt_nm_index.unstack()
    ym_dt_index_name_col.columns = ym_dt_index_name_col.columns.droplevel(0)
    return ym_dt_index_name_col.groupby(level=0)


def concat_fillna(before: pd.DataFrame, after: pd.DataFrame):
    index = before.index.union(after.index)
    columns = before.columns.union(after.columns).sort_values()
    return pd.DataFrame(columns=columns, index=index).fillna(after).fillna(before)


def save_csv(ym_dt_n_t):
    for ym, dt in groupby(ym_dt_n_t):
        fp = DB_PATH / f"{ym}.csv"
        db = pd.DataFrame(columns=["DT"]).set_index("DT")
        if Path(fp).exists():
            db = pd.read_csv(fp, index_col="DT", encoding="utf-8")
        to_merge = dt.droplevel(level=0, axis=0)
        concat_fillna(db, to_merge).to_csv(fp, encoding="utf-8")
