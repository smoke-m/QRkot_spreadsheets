from sqlalchemy import Column, ForeignKey, Integer

from app.core.db import Base


class DonatsInProjs(Base):

    donation_id = Column(Integer, ForeignKey('donation.id'))
    project_id = Column(Integer, ForeignKey('charityproject.id'))
    ivisted = Column(Integer,)

    def create(self, cls, target_id, source_id, ivisted):
        if cls == 'Donation':
            self.donation_id = target_id
            self.project_id = source_id
        elif cls == 'CharityProject':
            self.donation_id = source_id
            self.project_id = target_id
        self.ivisted = ivisted
