import streamlit as st
import requests
import plotly.graph_objs as go

# Placeholder planetary data – can be replaced with real API
def get_planet_data():
    planets = {
        "Mercury": {"radius": 2439.7, "distance": 57.91},
        "Venus": {"radius": 6051.8, "distance": 108.2},
        "Earth": {"radius": 6371, "distance": 149.6},
        "Mars": {"radius": 3389.5, "distance": 227.9},
        "Jupiter": {"radius": 69911, "distance": 778.5},
        "Saturn": {"radius": 58232, "distance": 1433.5},
        "Uranus": {"radius": 25362, "distance": 2872.5},
        "Neptune": {"radius": 24622, "distance": 4495.1},
    }
    return planets

# Fetch NASA image of the selected planet
def fetch_planet_image(planet_name):
    url = f"https://images-api.nasa.gov/search?q={planet_name}&media_type=image"
    response = requests.get(url)
    data = response.json()
    
    try:
        image_url = data['collection']['items'][0]['links'][0]['href']
        return image_url
    except:
        return None

# Show selected planet info in sidebar
def display_planet_info(planet_name):
    planets = get_planet_data()
    planet_data = planets.get(planet_name)
    
    if planet_data:
        st.sidebar.markdown(f"### 🌍 {planet_name}")
        st.sidebar.write(f"**Radius:** {planet_data['radius']} km")
        st.sidebar.write(f"**Distance from Sun:** {planet_data['distance']} million km")
        
        image_url = fetch_planet_image(planet_name)
        if image_url:
            st.sidebar.image(image_url, caption=f"{planet_name} (NASA)", use_column_width=True)
        else:
            st.sidebar.write("No image found for this planet.")

# Create a 3D Solar System Model using Plotly
def create_solar_system():
    planets = get_planet_data()
    trace = []

    for planet, data in planets.items():
        trace.append(go.Scatter3d(
            x=[data["distance"]],
            y=[0],
            z=[0],
            mode='markers+text',
            marker=dict(size=max(data["radius"] / 3000, 5)),  # Min size to keep small planets visible
            text=[planet],
            textposition='top center'
        ))

    layout = go.Layout(
        title="🌌 Interactive Solar System",
        scene=dict(
            xaxis_title='Distance from Sun (in million km)',
            yaxis_title='',
            zaxis_title=''
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False
    )

    fig = go.Figure(data=trace, layout=layout)
    return fig

# Main App
def main():
    st.set_page_config(page_title="Interactive Solar System", layout="wide")
    st.title("🪐 Interactive Solar System")
    st.write("Explore the solar system and learn more about each planet.")

    # 3D Plot
    fig = create_solar_system()
    st.plotly_chart(fig, use_container_width=True)

    # Sidebar Info
    planet_name = st.sidebar.selectbox("🔭 Select a planet:", list(get_planet_data().keys()))
    display_planet_info(planet_name)

if __name__ == '__main__':
    main()
