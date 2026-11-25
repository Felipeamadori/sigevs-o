package br.com.pdsars.sigevs.competency;

import br.com.pdsars.sigevs.dto.premise.PremiseDTO;
import br.com.pdsars.sigevs.dto.premise.PremiseLocationDTO;
import br.com.pdsars.sigevs.dto.registration.CARShape;
import br.com.pdsars.sigevs.dto.registration.ModuloDTO;
import br.com.pdsars.sigevs.dto.registration.UsuarioDTO;
import br.com.pdsars.sigevs.enums.SysEventType;
import br.com.pdsars.sigevs.mappers.PremiseMapper;
import br.com.pdsars.sigevs.model.registration.Endereco;
import br.com.pdsars.sigevs.model.registration.Frigorifico;
import br.com.pdsars.sigevs.model.registration.CadastroAmbientalRural;
import br.com.pdsars.sigevs.model.registration.Estabelecimento;
import br.com.pdsars.sigevs.model.registration.Modulo;
import br.com.pdsars.sigevs.model.registration.Usuario;
import br.com.pdsars.sigevs.repository.registration.CARRepository;
import br.com.pdsars.sigevs.repository.registration.EstabelecimentoRepository;
import br.com.pdsars.sigevs.repository.registration.ModuloRepository;
import br.com.pdsars.sigevs.repository.registration.UsuarioRepository;
import br.com.pdsars.sigevs.service.SysEventLoggerService;
import br.com.pdsars.sigevs.service.registration.CARService;
import br.com.pdsars.sigevs.service.registration.ModuloService;
import br.com.pdsars.sigevs.service.registration.PremiseService;
import br.com.pdsars.sigevs.service.registration.UsuarioService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.data.domain.Sort;

import java.math.BigDecimal;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

/**
 * Unit tests for the Core subdomain competency questions (CQ-CORE-01..07).
 *
 * One test per competency question; all collaborators are mocked (no database).
 */
@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class CoreCompetencyQuestionsTest {

    @Mock private EstabelecimentoRepository estabelecimentoRepository;
    @Mock private PremiseMapper premiseMapper;
    @Mock private SysEventLoggerService sysEventLoggerService;

    @Mock private CARRepository carRepository;
    @Mock private UsuarioRepository usuarioRepository;
    @Mock private br.com.pdsars.sigevs.service.integration.KeycloakUserService keycloakUserService;
    @Mock private ModuloRepository moduloRepository;

    private PremiseService premiseService() {
        return new PremiseService(estabelecimentoRepository, premiseMapper, sysEventLoggerService);
    }

    private Estabelecimento estabelecimento() {
        Estabelecimento estabelecimento = new Estabelecimento();
        estabelecimento.setCodigoEstabelecimento("SDA-001");
        estabelecimento.setNomeEstabelecimento("Granja Sao Joao");
        estabelecimento.setAtivo(true);
        return estabelecimento;
    }

    @Test
    @DisplayName("CQ-CORE-01 — Quais estabelecimentos rurais estão cadastrados no sistema?")
    void cqCore01() {
        Estabelecimento entity = estabelecimento();
        when(estabelecimentoRepository.findByCodigoEstabelecimento("SDA-001"))
                .thenReturn(java.util.Optional.of(entity));
        PremiseDTO dto = new PremiseDTO();
        dto.setCodigoSda("SDA-001");
        dto.setNomeFantasia("Granja Sao Joao");
        when(premiseMapper.toDto(entity)).thenReturn(dto);

        PremiseDTO result = premiseService().searchByCode("SDA-001");

        assertEquals("SDA-001", result.getCodigoSda());
        assertFalse(result.getNomeFantasia().isBlank());
    }

    @Test
    @DisplayName("CQ-CORE-02 — Quais espécies animais são exploradas em cada estabelecimento?")
    void cqCore02() {
        Estabelecimento entity = estabelecimento();
        entity.setEspecies(List.of("AVES", "SUINOS"));
        when(estabelecimentoRepository.findByCodigoEstabelecimento("SDA-001"))
                .thenReturn(java.util.Optional.of(entity));
        PremiseDTO dto = new PremiseDTO();
        dto.setEspecies(List.of("AVES", "SUINOS"));
        when(premiseMapper.toDto(entity)).thenReturn(dto);

        PremiseDTO result = premiseService().searchByCode("SDA-001");

        assertEquals(List.of("AVES", "SUINOS"), result.getEspecies());
    }

    @Test
    @DisplayName("CQ-CORE-03 — Qual a localização geográfica (coordenadas) de um estabelecimento?")
    void cqCore03() {
        Estabelecimento entity = estabelecimento();
        entity.setId(7L);
        Endereco endereco = new Endereco();
        entity.setEndereco(endereco);
        when(estabelecimentoRepository.findByCodigoEstabelecimentoWithEndereco("SDA-001"))
                .thenReturn(java.util.Optional.of(entity));
        when(estabelecimentoRepository.save(entity)).thenReturn(entity);
        when(premiseMapper.toDto(entity)).thenReturn(new PremiseDTO());

        premiseService().updateLocation("SDA-001",
                new PremiseLocationDTO(new BigDecimal("-29.6886"), new BigDecimal("-51.4611")));

        assertEquals(new BigDecimal("-29.6886"), entity.getEndereco().getLatitude());
        assertEquals(new BigDecimal("-51.4611"), entity.getEndereco().getLongitude());
        verify(estabelecimentoRepository).save(entity);
        verify(sysEventLoggerService).logEntityChange(eq(SysEventType.UPDATE), eq(Estabelecimento.class), eq(7L),
                any(PremiseDTO.class), any(PremiseDTO.class));
    }

    @Test
    @DisplayName("CQ-CORE-04 — Quais profissionais estão cadastrados no serviço veterinário? (resolvida na camada JPA)")
    void cqCore04() {
        Usuario usuario = new Usuario();
        usuario.setIdUsuario(1);
        usuario.setNome("Maria Silva");
        when(usuarioRepository.findById(1)).thenReturn(java.util.Optional.of(usuario));

        UsuarioService usuarioService = new UsuarioService(
                usuarioRepository, keycloakUserService, moduloRepository);
        UsuarioDTO dto = usuarioService.findById(1L);

        assertNotNull(dto);
    }

    @Test
    @DisplayName("CQ-CORE-05 — Qual o perímetro geográfico (CAR) de uma propriedade?")
    void cqCore05() {
        CadastroAmbientalRural car = new CadastroAmbientalRural();
        car.setCarShape("{\"type\":\"Polygon\",\"features\":[]}");
        when(carRepository.findByCidade("montenegro")).thenReturn(car);

        CARService carService = new CARService(carRepository, new ObjectMapper());
        CARShape shape = carService.getCarDataCidade("Montenegro");

        assertNotNull(shape);
        assertEquals("Polygon", shape.getType());
    }

    @Test
    @DisplayName("CQ-CORE-06 — Quais estabelecimentos possuem inspeção (SIF/SIE/SIM) e qual o tipo?")
    void cqCore06() {
        Estabelecimento entity = estabelecimento();
        entity.setTipo("Frigorífico");
        Frigorifico frigorifico = new Frigorifico();
        frigorifico.setEstabelecimento(entity);
        frigorifico.setSistemaInspecao("SIF");
        frigorifico.setNumeroInspecao("12/SSMA");

        assertEquals("Frigorífico", frigorifico.getEstabelecimento().getTipo());
        assertEquals("SIF", frigorifico.getSistemaInspecao());
        assertTrue(List.of("SIF", "SIE", "SIM").contains(frigorifico.getSistemaInspecao()));
    }

    @Test
    @DisplayName("CQ-CORE-07 — Quais módulos/perfis do sistema um profissional pode acessar?")
    void cqCore07() {
        Modulo cadastros = new Modulo();
        cadastros.setIdModulo(1);
        cadastros.setNome("Cadastro");
        Modulo spread = new Modulo();
        spread.setIdModulo(2);
        spread.setNome("Spread");
        when(moduloRepository.findAll(any(Sort.class))).thenReturn(List.of(cadastros, spread));

        ModuloService moduloService = new ModuloService(moduloRepository);
        List<ModuloDTO> modulos = moduloService.findAllAvailable();

        assertEquals(2, modulos.size());
    }
}
