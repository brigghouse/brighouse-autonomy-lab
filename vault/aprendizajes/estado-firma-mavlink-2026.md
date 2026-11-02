---
title: Estado de la firma MAVLink en 2026 (resumen para ventas)
date: 2026-11-02
tags: [aprendizaje, mavlink, cra, ventas]
---

# Estado de la firma MAVLink en 2026: lo que hay que saber de memoria

- **PX4:** la firma conforme a la especificación llega con la **v1.18** (en beta a 2026-11-02, PR #26894). Viene **desactivada por defecto**. El primer `SETUP_SIGNING` se acepta sin firma por cualquier enlace (*trust-on-first-use*), así que quien provisiona primero se queda con el control.
- **ArduPilot:** la firma se activa desde Mission Planner o MAVProxy. **USB queda exento**, la telemetría de bajada va sin firma y los puertos MAVLink 1 no quedan protegidos.
- **CISA ICSA-26-090-02 / CVE-2026-1579 (CVSS 9.8):** MAVLink sin firma en PX4. La solución es activar la firma. **Es el mejor gancho de venta:** "tu dron tiene un aviso de CISA de 9,8 si no activaste la firma".
- **Grupo de CVE de PX4 en 2026** (FTP, shell y log handler): cualquiera los alcanza si la firma está desactivada.
- **El CRA cubre los drones con marcado de clase C (2019/945).** Solo excluye los *certificados* según 2018/1139. El fabricante que integra PX4 o ArduPilot asume todo el anexo I. Esto es interpretación nuestra, no asesoramiento jurídico.
- **2019/945, clase C2 (y probablemente C3):** el enlace C2 debe estar "protegido contra el acceso no autorizado". No dice cómo, y ahí encaja nuestro informe.
- **Nadie ha publicado una tabla de correspondencias entre MAVLink, el CRA y la 2019/945.** Es el valor diferencial del Paper 1.

Fuente completa: [revisión bibliográfica](../../research/literature-review.md) · Borrador: [Paper 1](../../paper/paper1-draft.md)

Related: [Oferta](../proyecto/oferta.md) · [pymavlink y MAVLink 2](pymavlink-mavlink2.md)
