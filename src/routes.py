from flask import Blueprint, Response, render_template
from src.services.camera import generate_frames

bp = Blueprint('main', __name__)

@bp.route('/')                                                                                                                                            
@bp.route('/index.html')                                                                                                                             
def index():                                                                                                                                
    """Video streaming home page."""                                                                                                        
    return render_template('index.html')

@bp.route('/historical_images.html')                                                                                                                    
def historical_images():                                                                                                                    
    """Historical images page."""                                                                                                        
    return render_template('historical_images.html')

@bp.route('/notifications.html')                                                                                                                    
def live_videos():                                                                                                                    
    """Notifications page."""                                                                                                        
    return render_template('notifications.html')

@bp.route('/statistics.html')                                                                                                                    
def statistics():                                                                                                                    
    """Statistics page."""                                                                                                        
    return render_template('statistics.html')

@bp.route('/video_feed')                                                                                                                   
def video_feed():                                                                                                                           
    """Video streaming route. Put this in the src attribute of an img tag."""                                                               
    return Response(generate_frames(),                                                                                                      
                    mimetype='multipart/x-mixed-replace; boundary=frame')