"""
Author: Jacob Dallas
"""
from MyMarketNewsUSDA.ApiBase import ApiBase


class Report(ApiBase):
    """
    This class is used to store the data from a single report and provide methods to manipulate that data
    """
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("api_key", None))
        self.slug_id = kwargs.get("slug_id", None)
        if self.slug_id is None:
            self.data = None

        # get the report data
        self.report_url = self.create_api_url(slug_id=self.slug_id)
        self.data = self.get_data(self.report_url)

    def set_slug_id(self, slug_id: str) -> None:
        """
        Sets the slug_id of the report, then gathers the data for that report
        :param slug_id: The slug_id to be set
        :return: None
        """
        self.slug_id = slug_id
        self.report_url = self.create_api_url(slug_id=self.slug_id)
        self.data = self.get_data(self.report_url)

    def __repr__(self):
        return f"Report(slug_id={self.slug_id})"

    def __str__(self):
        return f"Report(slug_id={self.slug_id})"




