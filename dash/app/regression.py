from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import numpy as np

def create_lin_reg_plot(X, y, x_axis, y_axis, title):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=67)
    model = LinearRegression().fit(X_train, y_train)
    y_pred = model.predict(X_test)
    x_vals = np.asarray(X_test).ravel()
    y_vals = np.asarray(y_test).ravel()
    y_pred = np.asarray(y_pred).ravel()
    order = x_vals.argsort()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_vals, y=y_vals,
        mode="markers",
        marker=dict(opacity=0.6),
        name="Actual data",
    ))
    fig.add_trace(go.Scatter(
        x=x_vals[order], y=y_pred[order],
        mode="lines",
        line=dict(color="red"),
        name="Predicted data",
    ))
    fig.update_layout(
        xaxis_title=x_axis,
        yaxis_title=y_axis,
        title=title,
    )
    return fig