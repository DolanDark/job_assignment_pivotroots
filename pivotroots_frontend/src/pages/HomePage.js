function HomePage() {

    const centerStyle = {
		margin: "auto",
		width: "50%",
		padding: "10px"
	}

    return (
        <div style={centerStyle}>
            <h3>The app is up and running....</h3>
            <br/>
            <p>The routes in this app are as follows</p>
            <p>
            / (GET, POST)<br/>
            /login (POST)<br/>
            /register (POST)<br/>
            /user-page (GET)<br/>
            /documents/&lt;folder&gt;/&lt;filename&gt;&lt;/filename&gt; (GET, POST)
            <br/><br/>the repo also contains the postman collection for this app
            </p>
        </div>
    )

}

export default HomePage