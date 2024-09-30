from flask import *
import plotly.graph_objs as go
import numpy as np
from urllib.parse import quote
import matplotlib.pyplot as plt
import io
import random
import random
import time

app = Flask(__name__)

################
#  DB Connection  #
################

# MySQL database connection configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'spectro'
}


# Create a connection to the database
def get_db_connection(mysql=None):
    conn = mysql.connector.connect(**db_config)
    return conn


# Route to test database connection
@app.route('/test-db', methods=['GET'])
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Cursor to execute queries
        cursor.execute("SELECT * FROM log LIMIT 5")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return str(e)


@app.route('/add-user', methods=['POST'])
def add_user():
    try:

        name = "sanchitha"
        age = 23

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO log (name, age) VALUES (%s, %s)", (name, age))
        conn.commit()  # Commit the transaction
        cursor.close()
        conn.close()
        return jsonify({"message": "User added successfully!"})
    except Exception as e:
        return str(e)


@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM log")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users)
    except Exception as e:
        return str(e)


################
#  UI Routing  #
################

@app.route('/')
def splash():
    return render_template('statSegments/splash.html')


@app.route('/navigate_to_index')
def navigate_to_index():
    return render_template('index.html')


@app.route('/analyze')
def analyze():
    return render_template('analyze.html')


# Route for Directories page
@app.route('/directories')
def directories():
    return render_template('directories.html')


# Route for Spectrum page
@app.route('/spectrum')
def spectrum():
    return render_template('analyze.html')


# Route for Models page
@app.route('/models')
def models():
    return render_template('models.html')


# Route for Activity Log page
@app.route('/activity-log')
def activity_log():
    return render_template('activity_log.html')


# Route for Settings page
@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/appType')
def appType():
    return render_template('appType.html')


@app.route('/absorbance')
def absorbance():
    return render_template('absorbance.html')


@app.route('/reflectance')
def reflectance():
    return render_template('reflectance.html')


@app.route('/transmission')
def transmission():
    return render_template('transmission.html')


@app.route('/absorbanceParameters')
def absorbanceParameters():
    return render_template('absorbanceParameters.html')


@app.route('/reflectanceParameters')
def reflectanceParameters():
    return render_template('reflectanceParameters.html')


@app.route('/transmissionParameters')
def transmissionParameters():
    return render_template('transmissionParameters.html')


@app.route('/whiteReference')
def whiteReference():
    return render_template('whiteReferance.html')


@app.route('/darkReference')
def darkReference():
    return render_template('darkReferance.html')


@app.route('/calibratePlot')
def calibratePlot():
    return render_template('calibratePlot.html')


#####################
#  Python functions #
#####################

# Function to simulate updating plot data
# Route to serve the live-updating chart image
# Route to generate the plot dynamically
@app.route('/plot-data')
def plot_data():
    # Example sensor data: Replace with actual sensor data retrieval
<<<<<<< HEAD
    x = [595, 595, 596, 596, 595, 596, 597, 595, 595, 596, 596, 595, 596, 593, 595, 596, 595, 596, 597, 594, 595, 596,
         591, 595, 597, 593, 595, 595, 594, 595, 598, 593, 595, 596, 595, 595, 597, 593, 593, 598, 598, 594, 609, 608,
         598, 595, 600, 593, 593, 596, 591, 595, 595, 595, 595, 595, 595, 595, 593, 594, 595, 595, 595, 595, 595, 600,
         593, 593, 602, 594, 595, 605, 597, 595, 600, 590, 590, 593, 594, 591, 595, 593, 594, 596, 595, 593, 595, 595,
         595, 595, 595, 594, 595, 596, 583, 591, 600, 590, 595, 595, 593, 595, 600, 593, 595, 600, 591, 596, 598, 593,
         594, 595, 594, 596, 596, 591, 593, 596, 596, 596, 598, 598, 595, 594, 597, 595, 591, 600, 595, 593, 595, 595,
         595, 595, 591, 595, 595, 595, 595, 595, 595, 595, 594, 600, 595, 593, 600, 593, 594, 597, 593, 596, 595, 591,
         598, 600, 595, 596, 600, 591, 597, 595, 591, 595, 595, 594
         ]
    y = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
         0.3, 0.3, 0.5, 1.3, 1.5, 2.3, 2.5, 3.3, 3.5, 1.3, 1.5, 2.3, 2.5, 3.3, 3.5, 4.3, 4.5, 2.3, 2.5, 3.3, 3.5, 4.3,
         4.5, 5.3, 5.5, 3.3, 3.5, 4.3, 4.5, 5.3, 5.5, 6.3, 6.5, 4.3, 4.5, 5.3, 5.5, 6.3, 6.5, 7.3, 7.5, 5.3, 5.5, 6.3,
         6.5, 7.3, 7.5, 8.3, 8.5, 6.3, 6.5, 7.3, 7.5, 8.3, 8.5, 9.3, 9.5, 7.3, 7.5, 8.3, 8.5, 9.3, 9.5, 10.3, 10.5, 8.3,
         8.5, 9.3, 9.5, 10.3, 10.5, 11.3, 11.5, 9.3, 9.5, 10.3, 10.5, 11.3, 11.5, 12.3, 12.5, 10.3, 10.5, 11.3, 11.5,
         12.3, 12.5, 13.3, 13.5, 11.3, 11.5, 12.3, 12.5, 13.3, 13.5, 14.3, 14.5, 12.3, 12.5, 13.3, 13.5, 14.3, 14.5,
         15.3, 15.5, 13.3, 13.5, 14.3, 14.5, 15.3, 15.5, 16.3, 16.5, 14.3, 14.5, 15.3, 15.5, 16.3, 16.5, 17.3, 17.5,
         15.3, 15.5, 16.3, 16.5, 17.3, 17.5, 18.3, 18.5, 16.3, 16.5, 17.3, 17.5, 18.3, 18.5, 19.3, 19.5, 17.3, 17.5,
         18.3, 18.5, 19.3, 19.5, 20.3
         ]
=======
    y = [0.986130537, 0.934567681, 0.955928545, 0.88649236, 0.974375868, 0.98904996, 0.841716833, 0.828722015,
         0.893976276, 0.832195949, 0.836127645, 0.917858404, 0.845945889, 0.992145657, 0.904151376, 0.933519638,
         0.904025549, 0.897803434, 0.885960055, 0.821355549, 0.983371006, 0.905645, 0.914920046, 0.982508633,
         0.903279402, 0.88058903, 0.922680174, 0.827214872, 0.956493765, 0.955346919, 0.932484519, 0.817502202,
         0.945659235, 0.830260061, 0.915168381, 0.850923016, 0.995457052, 0.999564292, 0.908917814, 0.922943168,
         0.881096178, 0.903347299, 0.901377787, 0.971693443, 0.936706874, 0.996383268, 0.951604933, 0.808069144,
         0.964861945, 0.945336196, 0.903372409, 0.933358442, 0.905542107, 0.877522036, 0.904303753, 0.9736246,
         0.888992392, 0.981129797, 0.915052314, 0.885935699, 0.951788622, 0.853757621, 0.968260963, 0.828673631,
         0.865620296, 0.85342043, 0.870728066, 0.871152689, 0.93198085, 0.962149528, 0.899409372, 0.913979063,
         0.973940486, 0.841222237, 0.943253978, 0.824343874, 0.811255779, 0.922281355, 0.828341661, 0.860470024,
         0.837711347, 0.88931191, 0.838275917, 0.941838782, 0.954788448, 0.925480711, 0.902221738, 0.956275097,
         0.870862882, 0.80939929, 0.942693718, 0.818916172, 0.956410807, 0.845931461, 0.883850528, 0.86386461,
         0.91604529, 0.901428181, 0.988724335, 0.871038994, 0.864601184, 0.826574638, 0.818506917, 0.916780872,
         0.97240711, 0.98682363, 0.819566994, 0.976182061, 0.821518488, 0.874266795, 0.848423315, 0.993139495,
         0.994169804, 0.812301919, 0.947672824, 0.984580888, 0.915984686, 0.853191388, 0.857420362, 0.958767159,
         0.869472876, 0.905821709, 0.952349648, 0.922272466, 0.892787474, 0.82713998, 0.987033202, 0.977151472,
         0.86509443, 0.84605117, 0.872623867, 0.969210265, 0.912856269, 0.976876293, 0.957349657, 0.879219017,
         0.899547854, 0.82270915, 0.941716521, 0.922967853, 0.809778794, 0.928511229, 0.911071704, 0.816347248,
         0.851269282, 0.963431127, 0.928115096, 0.840959228, 0.934574274, 0.902385573, 0.948732289, 0.824259325,
         0.878340719, 0.977066903, 0.845932168, 0.82784246, 0.886833136, 0.948381013, 0.860462996, 0.837460478,
         0.96388668, 0.986110962, 0.999007908, 0.889056469, 0.933736313, 0.904556391, 0.933061502, 0.911115597,
         0.879095474, 0.951607285, 0.914623928, 0.980529515, 0.978245931, 0.876012378, 0.905616323, 0.843454227,
         0.943113694, 0.909695551, 0.818695071, 0.87355884, 0.91235679, 0.946910043, 0.803962568, 0.833479033,
         0.980772542, 0.867535322, 0.862788939, 0.86289584, 0.813778982, 0.928664287, 0.959749728, 0.818147407,
         0.83459591, 0.943311214, 0.99495298, 0.942343022, 0.99791746, 0.836678517, 0.95787928, 0.821719691,
         0.837395054, 0.886846582, 0.830746432, 0.982157935, 0.828591347, 0.966538948, 0.876553292, 0.99679809,
         0.845647722, 0.910630241, 0.937512167, 0.980459982, 0.859510993, 0.851742752, 0.895070649, 0.822865624,
         0.925615057, 0.878886434, 0.897768387, 0.814303411, 0.918095899, 0.88183242, 0.993077051, 0.905128242,
         0.827403049, 0.999696295, 0.846142958, 0.832252684, 0.842241831, 0.83673147, 0.953350573, 0.946950778,
         0.912156995, 0.951716075, 0.924350144, 0.882392783, 0.828779578, 0.895689659, 0.908331656, 0.94792658,
         0.940887246, 0.921016715, 0.811490121, 0.885346011, 0.871883052, 0.84639946, 0.977333195, 0.9782623,
         0.846065837, 0.920392426, 0.888686439, 0.891512588, 0.823305436, 0.966557934, 0.897166856, 0.959575448,
         0.865316396, 0.993666239, 0.89932673, 0.999348093, 0.957151462, 0.94165204, 0.810363982, 0.817219296,
         0.890373199, 0.926778253, 0.917274482, 0.998369854, 0.831941202, 0.955394762, 0.978690529, 0.867588464,
         0.99958904, 0.867673875, 0.853670043, 0.981799505, 0.839682812, 0.897039029, 0.828329286, 0.824478811,
         0.804120547, 0.812871302, 0.948282861, 0.915588727, 0.877035931, 0.997074301, 0.849498218, 0.95186683,
         0.974959291, 0.905801817, 0.980551
         ]
    x = np.linspace(300, 900, 2088)
>>>>>>> parent of af558bc (plots updated)

    # Create a Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Sensor Data'))
    fig.update_layout(
<<<<<<< HEAD
        xaxis_title="waves",
        yaxis_title="Absorbance",
=======
        xaxis_title="Wavelength nm",
        yaxis_title="Reflectance%",
>>>>>>> parent of af558bc (plots updated)
        height=320,  # Set height to fit 480x320 resolution
        width=480
    )

    # Define the custom configuration for the toolbar
    config = {
        'displaylogo': False,  # Remove the Plotly logo
        'modeBarButtonsToRemove': ['lasso2d', 'autoScale2d', 'hoverClosestCartesian',
                                   'hoverCompareCartesian', 'zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'resetScale2d',
<<<<<<< HEAD
                                   'select2d', 'toggleSpikelines', 'toImage']
    }

    graphJSON = fig.to_json()
    return jsonify({'figure': graphJSON, 'config': config})


# New route for the second plot with different data
@app.route('/plot-data2')
def plot_data2():
    # Different dataset for the second plot
    y = np.random.random(100)  # Example random data
    x = np.linspace(200, 1000, 100)

    # Create a different Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Sensor Data 2'))
    fig.update_layout(
        xaxis_title="Wavelength nm",
        yaxis_title="Absorbance ( Dark )",
        height=320,
        width=480
    )

    # Custom toolbar configuration
    config = {
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'autoScale2d', 'hoverClosestCartesian',
                                   'hoverCompareCartesian', 'zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'resetScale2d',
                                   'select2d', 'toggleSpikelines', 'toImage']
    }

    graphJSON = fig.to_json()
    return jsonify({'figure': graphJSON, 'config': config})


# New route for the third plot with different data
@app.route('/plot-data3')
def plot_data3():
    # Different dataset for the second plot
    y = np.random.random(2088)  # Example random data
    x = np.linspace(300, 900, 100)

    # Create a different Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Sensor Data 3'))
    fig.update_layout(
        xaxis_title="Wavelength nm",
        yaxis_title="Absorbance ( White )",
        height=320,
        width=480
    )

    # Custom toolbar configuration
    config = {
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'autoScale2d', 'hoverClosestCartesian',
                                   'hoverCompareCartesian', 'zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'resetScale2d',
                                   'select2d', 'toggleSpikelines', 'toImage']
    }

    graphJSON = fig.to_json()
    return jsonify({'figure': graphJSON, 'config': config})


# New route for the forth plot with different data
@app.route('/plot-data4')
def plot_data4():
    # Different dataset for the second plot
    y = np.random.random(100)  # Example random data
    x = np.linspace(300, 900, 50)

    # Create a different Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Sensor Data 3'))
    fig.update_layout(
        xaxis_title="Wavelength nm",
        yaxis_title="Absorbance",
        height=320,
        width=480
    )

    # Custom toolbar configuration
    config = {
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'autoScale2d', 'hoverClosestCartesian',
                                   'hoverCompareCartesian', 'zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'resetScale2d',
                                   'select2d', 'toggleSpikelines', 'toImage']

=======
                                   'select2d', 'toggleSpikelines', 'toImage'
                                   ],  # Remove unwanted buttons
        # 'modeBarButtonsToAdd': ['zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'resetScale2d', 'select2d',
        #                         ],  # Add custom buttons
>>>>>>> parent of af558bc (plots updated)
    }

    # Convert plotly figure to JSON
    graphJSON = fig.to_json()
    return jsonify({'figure': graphJSON, 'config': config})


###################
#  Main Function  #
###################

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
