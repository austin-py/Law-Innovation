from classes.CompanyStats import CompanyStats
from classes.WarningLetterStats import WarningLetterStats
from classes.InspectionLetterStats import InspectionLetterStats

class StatGrabber():
    def __init__(self,search_term, inspection_df,warning_df) -> None:
        self.inspect_data = inspection_df
        self.warning_data = warning_df
        self.CompanyStats = CompanyStats(inspection_df)
        self.WarningLetterStats = WarningLetterStats(search_term, warning_df)
        self.InspectionLetterStats = InspectionLetterStats(search_term, inspection_df)