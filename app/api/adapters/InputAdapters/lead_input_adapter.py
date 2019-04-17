from flask_restful import reqparse


class LeadInputAdapter():

    TITLE = "title"
    LEAD_DESCRIPTION = "lead_description"
    CATEGORY = "category"
    SUBCATEGORY = "subcategory"
    PRICE = "price"
    TAG = "tag"
    SCORE = "score"
    FEATURES = "featured"
    LAST_UPDATED_ON = "last_updated_on"

    def parse(self):
        parser = reqparse.RequestParser()
        parser.add_argument(self.TITLE, required=False, type=str)
        parser.add_argument(self.LEAD_DESCRIPTION, required=False, type=str)
        parser.add_argument(self.CATEGORY, required=False, type=str)
        parser.add_argument(self.SUBCATEGORY, required=False, type=str)
        parser.add_argument(self.PRICE, required=False, type=str)
        parser.add_argument(self.TAG, required=False, type=str)
        parser.add_argument(self.SCORE, required=False, type=str)
        parser.add_argument(self.FEATURES, required=False, type=str)
        parser.add_argument(self.LAST_UPDATED_ON, required=False, type=str)
        return parser.parse_args()
