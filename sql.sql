-- Crear la tabla de usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    correo VARCHAR(255) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL
);

-- Insertar datos de prueba en la tabla usuarios
INSERT INTO usuarios (correo, contraseña) VALUES
('usuario1@example.com', 'password1'),
('usuario2@example.com', 'password2'),
('usuario3@example.com', 'password3');
