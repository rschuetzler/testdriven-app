import React from 'react';
import { Redirect } from 'react-router-dom';

const Form = (props) => {
    if (props.isAuthenticated) {
        return <Redirect to="/" />
    }
    return (
        <div>
            <h1>{props.formType}</h1>
            <hr /><br />
            <form onSubmit={(event) => props.handleUserFormSubmit(event)}>
                {props.formType === 'Register' &&
                    <div className="form-group">
                        <input type="text"
                            name="username"
                            className="form-control input-lg"
                            placeholder="Enter a username"
                            required
                            value={props.formData.username}
                            onChange={props.handleFormChange}
                        />
                    </div>
                }
                <div className="form-group">
                    <input
                        type="email"
                        name="email"
                        className="form-control input-lg"
                        placeholder="Enter an email address"
                        required
                        value={props.formData.email}
                        onChange={props.handleFormChange}
                    />
                </div>
                <div className="form-group">
                    <input
                        type="password"
                        name="password"
                        className="form-control input-lg"
                        placeholder="Enter a password"
                        required
                        value={props.formData.password}
                        onChange={props.handleFormChange}
                    />
                </div>
                <input type="submit" value="Submit" className="btn btn-primary btn-lg btn-block" />
            </form>
        </div>
    )
};

export default Form;
