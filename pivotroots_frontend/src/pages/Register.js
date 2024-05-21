import { useState } from 'react'
import { useHistory, Link } from 'react-router-dom'

function Register() {

	const history = useHistory()
	// const navigate = useNavigate();

	const centerStyle = {
		margin: "auto",
		width: "50%",
		padding: "10px"
	  }

	const [username, setUsername] = useState('')
	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')

	async function registerUser(event) {
		event.preventDefault()

		const response = await fetch('http://localhost:8080/register', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				"username": username,
				email,
				password,
			}),
		})

		if (response.status == 500) {
			alert('Something went wrong')
			history.push('/register')
		}

		const data = await response.json()

		if (data.status == 'success') {
			alert('User Successfully registered')
			history.push('/login')
		} else {
			alert(data.message)
		}

		// if (data.status === 'ok') {
		// 	history.push('/login')
		// 	// navigate('/login');
		// }
	}

	return (
		<div style={centerStyle}>
			<h1>Register</h1>
			<form onSubmit={registerUser}>
				<input
					value={username}
					onChange={(e) => setUsername(e.target.value)}
					type="text"
					placeholder="Username"
				/>
				<br />
				<input
					value={email}
					onChange={(e) => setEmail(e.target.value)}
					type="email"
					placeholder="Email"
				/>
				<br />
				<input
					value={password}
					onChange={(e) => setPassword(e.target.value)}
					type="password"
					placeholder="Password"
				/>
				<br />
				<input type="submit" value="Register" />
			</form>
			<br/>
			<Link to="/login"> Already have an account?</Link>
		</div>
	)
}

export default Register
