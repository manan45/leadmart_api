from app.api.adapters.OutputAdapters import UserOutputAdapter


class LeadOutputAdapter():

    def parse(self, lead):
        return{
            "lead_id": lead.id,
            "title": lead.title,
            "description": lead.lead_description,
            "category": lead.category,
            "subcategory": lead.sub_category,
            "price": lead.price,
            "tag": lead.tag,
            "features": lead.features,
            "score": lead.score,
            "user": UserOutputAdapter().parse(lead.user),
            "status": lead.status
        }
