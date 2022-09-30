from header import get_body_heats
from purify import convert_header_to_df
from save_csv import save_csv

save_csv(convert_header_to_df([body_heat for body_heat in get_body_heats()]))
