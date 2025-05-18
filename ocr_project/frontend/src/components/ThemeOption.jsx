import React from "react";

const ThemeOption = ({theme}) => {
    return (
        <div className="theme-option" id={`theme-${theme}`}></div>
    )
}

export default ThemeOption;