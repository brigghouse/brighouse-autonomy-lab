---
title: "Aprendizaje: pymavlink y MAVLink 2"
date: 2026-11-02
tags: [aprendizaje, mavlink, pymavlink]
---

# Aprendizaje: pymavlink y MAVLink 2

1. **`mavutil` usa el dialecto MAVLink 1 salvo que exista la variable de entorno `MAVLINK20`.** Sin ella, todo lo que envías sale como MAVLink 1 y la firma no funciona. mavaudit la activa en `mavaudit/__init__.py`. El parser de MAVLink 2 también lee tramas MAVLink 1.
2. **Detectar la firma sin la clave:** bit 0 de `incompat_flags` en la cabecera MAVLink 2 (`msg._header.incompat_flags & 0x01`). `msg.get_signed()` solo es True si el receptor tiene la clave y la firma es válida.
3. **MAVLink 1 empieza por 0xFE y MAVLink 2 por 0xFD.** El primer byte de `msg.get_msgbuf()` sirve para distinguirlos.
4. **Con la firma activada, pymavlink lanza `MAVError("Invalid signature")` al recibir un mensaje sin firma** (o lo convierte en BAD_DATA con `robust_parsing`), salvo que `allow_unsigned_callback` lo acepte.
5. **Los tests deben comprobar también el caso negativo** (por ejemplo, `v1_frames == 0` en modo MAVLink 2). Si no, un test puede pasar por casualidad.

Related: [Diario 2026-11-02](../diario/2026-11-02.md)
