# Cambio realizado por colaborador (Mejora y formato PEP 8)
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Configuración básica
Base = declarative_base()
engine = create_engine("sqlite:///personas.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Definición del modelo
class Persona(Base):
    __tablename__ = "personas"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    edad = Column(Integer)

# Crear la tabla en la base de datos si no existe
Base.metadata.create_all(engine)

# Función de interpretación
def interpretar_texto(texto):
    palabras = texto.lower().split()
    
    if len(palabras) >= 4 and palabras[0] == "agrega" and palabras[1] == "persona":
        nombre = palabras[2].capitalize()
        edad = int(palabras[3])
        nueva = Persona(nombre=nombre, edad=edad)
        session.add(nueva)
        session.commit()
        return f"Persona '{nombre}' agregada con edad {edad}."
        
    elif texto.lower() == "muestra todas las personas":
        personas = session.query(Persona).all()
        if personas:
            return "\n".join([f"{p.id}. {p.nombre} - {p.edad} años" for p in personas])
        return "No hay personas registradas."
        
    elif texto.lower().startswith("borra persona") and len(palabras) >= 3:
        nombre = palabras[2].capitalize()
        persona = session.query(Persona).filter_by(nombre=nombre).first()
        if persona:
            session.delete(persona)
            session.commit()
            return f"Persona '{nombre}' eliminada."
        return f"No se encontró a '{nombre}'."
        
    else:
        return "Instrucción no reconocida."

# Ciclo principal de ejecución
if __name__ == "__main__":
    print("=== Sistema Text-to-SQL Básico ===")
    print("Comandos disponibles:")
    print(" - agrega persona <nombre> <edad>")
    print(" - muestra todas las personas")
    print(" - borra persona <nombre>")
    print(" - salir\n")
    
    while True:
        comando = input("Escribe tu instrucción: ")
        if comando.lower() == "salir":
            break
        resultado = interpretar_texto(comando)
        print(resultado)     
