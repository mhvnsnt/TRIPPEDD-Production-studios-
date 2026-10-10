# macify compile-only shim

BDSup2Sub's GUI classes reference `org.simplericity.macify.eawt` (Mac OS menu
integration). That artifact is **not on Maven Central** (404 at
`org/simplericity/macify/`), and this VM's Maven cannot reach any repo through
the egress proxy anyway.

These four stub classes reproduce exactly the API surface the GUI code uses
(`Application`, `DefaultApplication`, `ApplicationListener`,
`ApplicationEvent`) so the project compiles. They are **never on the CLI
execution path** — the smoke test runs headless SUP→VobSub conversion, which
never touches Mac menu integration. On a machine with real Maven Central
access, replace the shim with the genuine macify dependency from pom.xml.
