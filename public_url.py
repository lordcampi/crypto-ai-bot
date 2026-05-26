from pyngrok import ngrok

print("🚀 Iniciando túnel público...")

try:

    tunnel = ngrok.connect(
        addr=8501,
        proto="http"
    )

    print("\n")
    print("🌐 LINK PUBLICO:")
    print(tunnel.public_url)
    print("\n")

except Exception as e:

    print("❌ ERROR:")
    print(e)

input("ENTER para cerrar...")