from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,Float, REAL,DateTime,Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import enum
from .database import Base

## IMPORTANT NOTE: SQLAlchemy does not allow us to modify an existing table.We have to drop it and create it again.However there are database migration tools such as ALEMBIC.
#  Which allows us to work around this limitation.
# !pip install alembic

# alembic --help

# alembic init alembic  --> This creates a directory for alembic and alembic.ini out of directory.

# alembic revision --help  



# from .database import Base


## CREATING A TABLE THROUGH ORM:
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default="TRUE",nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id"), nullable=False)    
    
    
    
    # The code below will create automatically another property for our post , so when we retrieve a post its going to return it and figure out a relationship between post and user.
    owner = relationship("User") ## Here we are not referencing the table , we are referencing the actual SQLALCHEMY class as below:  class User(Base):

    
    
    
class User(Base):  ## every class is gonna extend base , its a requirement of SQLALCHEMY model.
    __tablename__= "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    
class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer,primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    upvotes = Column(Integer)
    downvotes =  Column(Integer)
    
    #vote_direction = Column(String,) this is for later so that I can implement reddit type up/downvote system
        
class Event_Post(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True,nullable=False)
    event_title = Column(String, nullable=False)
    event_content = Column(String, nullable=False)
    event_date = Column(String, nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"))
    organizer_name = Column(String, nullable=False)
    
class Tutor_List(Base):
    __tablename__ = "tutor_lists"
    id = Column(Integer,primary_key=True, nullable=False)
    tutor_email = Column(String, ForeignKey("users.email",ondelete="CASCADE"),primary_key=True)
    tutor_grade = Column(Float, nullable=False) 
    tutor_class_name = Column(String, nullable=False)
    
    
class Be_Tutor(Base):
    __tablename__ = "be_tutor_posts"
    id = Column(Integer, primary_key=True,nullable=False,unique=True)
    tutor_profile_title = Column(String, nullable=False)
    tutor_profile_explanation = Column(String, nullable=False)
    tutor_faculty_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    tutor_gpa = Column(Float, nullable=False)
    hourly_rate =Column(Float)
    
    tutor_email = Column(String, ForeignKey("users.email",ondelete="CASCADE"),primary_key=True)
    
    
class Hire_Tutor(Base):
    __tablename__ = "hiring_tutors_posts"
    id = Column(Integer, primary_key=True,nullable=False)
    post_title = Column(String, nullable=False)
    post_content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    employer_email = Column(String, ForeignKey("users.email",ondelete="CASCADE"),primary_key=True)
    
 
 
class EnumForRatingScore(enum.Enum):
    one = 1
    two = 2 
    three = 3 
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10 
    
class Rating_Tutor(Base):
    __tablename__ = "rating_tutors"
    id = Column(Integer, primary_key=True, nullable=False) 
    user_email = Column(String, ForeignKey("users.email",ondelete="CASCADE"),primary_key=True)
    #Username (FK) (UserDetailsID if you change the primary key of the UserDetails table)
    tutor_profile_id = Column(Integer, ForeignKey("be_tutor_posts.id",ondelete="CASCADE"),primary_key=True)
    #PostID (FK)    
    RatingScore = Column(Integer)
    DateRated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
   # Rater_id = Column()
    
## In the app, you would then pull back every RankScore with that PostID and do the calculation based off a count of said PostID.
    