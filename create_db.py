from cartoonfilter_ds_project.webapp import db, create_app

db.create_all(app=create_app())