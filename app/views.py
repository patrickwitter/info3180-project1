import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from app.forms import Property_Form
from app.models import Property
from werkzeug.utils import secure_filename


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Project 1")


@app.route('/properties/create', methods=['GET', 'POST'])
def new_property():
    """Add a new property to database"""
    property_form = Property_Form()
    if property_form.validate_on_submit():
        title = property_form.title.data
        prop_type = property_form.property_type.data
        location = property_form.location.data
        price = property_form.price.data
        description = property_form.description.data
        bedrooms = property_form.bedrooms.data
        bathrooms = property_form.bathrooms.data
        photo = property_form.photo.data
        photo_filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
        new_property = Property(title, prop_type, location, price, description, bedrooms, bathrooms, photo_filename)
        db.session.add(new_property)
        db.session.commit()
        flash("New property successfully added", "success")
        return redirect(url_for('view_properties'))
    return render_template("new_property.html", form=property_form)


@app.route('/properties')
def view_properties():
    """Show all properties"""
    properties = db.session.execute(db.select(Property)).scalars()
    return render_template("properties.html", properties=properties)


@app.route('/properties/<propertyid>')
def show_property_info(propertyid):
    property = db.session.execute(db.select(Property).filter_by(id=propertyid)).scalar()
    return render_template("property.html", property=property)


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


@app.route('/properties/<propertyid>/photo')
def get_property_image(propertyid):
    property = db.session.execute(db.select(Property).filter_by(id=propertyid)).scalar()
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), property.photo_filename)