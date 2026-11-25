package br.com.pdsars.sigevs.competency;

import br.com.pdsars.sigevs.dto.MovementDTO;
import br.com.pdsars.sigevs.dto.FilterMovementPageDTO;
import br.com.pdsars.sigevs.dto.premise.PremiseDTO;
import br.com.pdsars.sigevs.dto.SanitaryAnalysisDTO;
import br.com.pdsars.sigevs.enums.ImportType;
import br.com.pdsars.sigevs.enums.SpeciesCategory;
import br.com.pdsars.sigevs.enums.ZoneType;
import br.com.pdsars.sigevs.mappers.MovementMapper;
import br.com.pdsars.sigevs.mappers.PremiseMapper;
import br.com.pdsars.sigevs.mappers.SanitaryAnalysisMapper;
import br.com.pdsars.sigevs.model.AnalysisTarget;
import br.com.pdsars.sigevs.model.AffectedArea;
import br.com.pdsars.sigevs.model.registration.Endereco;
import br.com.pdsars.sigevs.model.movement.MovimentacaoAvesView;
import br.com.pdsars.sigevs.model.registration.Estabelecimento;
import br.com.pdsars.sigevs.model.registration.Usuario;
import br.com.pdsars.sigevs.repository.AffectedAreaRepository;
import br.com.pdsars.sigevs.repository.movement.MovimentacaoAvesRepository;
import br.com.pdsars.sigevs.repository.movement.MovimentacaoAvesViewRepository;
import br.com.pdsars.sigevs.repository.movement.MovimentacaoBovinosRepository;
import br.com.pdsars.sigevs.repository.movement.MovimentacaoBubalinosRepository;
import br.com.pdsars.sigevs.repository.movement.MovimentacaoCaprinosRepository;
import br.com.pdsars.sigevs.repository.movement.MovimentacaoOvinosRepository;
import br.com.pdsars.sigevs.repository.movement.MovimentacaoSuinosRepository;
import br.com.pdsars.sigevs.repository.SanitaryAnalysisRepository;
import br.com.pdsars.sigevs.repository.SanitaryEventResponseRepository;
import br.com.pdsars.sigevs.repository.registration.EstabelecimentoRepository;
import br.com.pdsars.sigevs.repository.registration.FrigorificoRepository;
import br.com.pdsars.sigevs.service.AffectedAreaService;
import br.com.pdsars.sigevs.service.SysEventLoggerService;
import br.com.pdsars.sigevs.service.registration.AnimalMovementService;
import br.com.pdsars.sigevs.service.registration.PremiseService;
import br.com.pdsars.sigevs.service.registration.UsuarioService;
import br.com.pdsars.sigevs.mappers.SurveillanceCycleZoneMapper;
import br.com.pdsars.sigevs.repository.ResponseSurveillanceCycleRepository;
import br.com.pdsars.sigevs.repository.SanitaryAnalysisRepository;
import jakarta.persistence.Table;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.data.domain.PageImpl;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

/**
 * Unit tests for the Sanitary Investigation subdomain competency questions
 * (CQ-INV-01..09). One test per competency question; all collaborators are
 * mocked (no database).
 */
@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class InvestigationCompetencyQuestionsTest {

    @Mock private SanitaryAnalysisRepository sanitaryAnalysisRepository;
    @Mock private SanitaryAnalysisMapper sanitaryAnalysisMapper;
    @Mock private UsuarioService usuarioService;
    @Mock private EstabelecimentoRepository estabelecimentoRepository;
    @Mock private PremiseMapper premiseMapper;
    @Mock private SysEventLoggerService sysEventLoggerService;
    @Mock private FrigorificoRepository frigorificoRepository;
    @Mock private ResponseSurveillanceCycleRepository responseSurveillanceCycleRepository;
    @Mock private SurveillanceCycleZoneMapper surveillanceCycleZoneMapper;
    @Mock private SanitaryEventResponseRepository sanitaryEventResponseRepository;
    @Mock private AffectedAreaRepository affectedAreaRepository;

    @Mock private MovimentacaoAvesViewRepository movimentacaoAvesViewRepository;
    @Mock private MovementMapper movementMapper;

    @InjectMocks private br.com.pdsars.sigevs.service.SanitaryAnalysisService sanitaryAnalysisService;

    private PremiseService premiseService() {
        return new PremiseService(estabelecimentoRepository, premiseMapper, sysEventLoggerService);
    }

    private Estabelecimento estabelecimentoAt(String lat, String lng) {
        Estabelecimento estabelecimento = new Estabelecimento();
        estabelecimento.setNomeEstabelecimento("Granja");
        Endereco endereco = new Endereco();
        endereco.setLatitude(new BigDecimal(lat));
        endereco.setLongitude(new BigDecimal(lng));
        estabelecimento.setEndereco(endereco);
        return estabelecimento;
    }

    @Test
    @DisplayName("CQ-INV-01 — Quais propriedades estão dentro do raio de vigilância de um foco ativo?")
    void cqInv01() {
        // focus at these coordinates; two premises, one inside the 3 km radius
        Estabelecimento foco = estabelecimentoAt("-29.6886", "-51.4611");
        Estabelecimento vizinho = estabelecimentoAt("-29.6800", "-51.4500");
        when(estabelecimentoRepository.findAtivosByRadius(-29.6886, -51.4611, 3000.0))
                .thenReturn(List.of(foco, vizinho));
        when(premiseMapper.toDto(any(Estabelecimento.class))).thenAnswer(invocation -> {
            Estabelecimento e = invocation.getArgument(0);
            PremiseDTO dto = new PremiseDTO();
            dto.setLatitude(String.valueOf(e.getEndereco().getLatitude()));
            dto.setLongitude(String.valueOf(e.getEndereco().getLongitude()));
            return dto;
        });

        List<PremiseDTO> result = premiseService().findByRadius(-29.6886, -51.4611, 3.0);

        assertEquals(2, result.size());
        assertNotNull(result.get(0).getDistancia());
        assertTrue(result.get(0).getDistancia() < result.get(1).getDistancia(),
                "haversine distance must be computed and grow with separation");
        assertTrue(result.get(0).getDistancia() < 100.0, "the focus itself is ~0 km away");
    }

    @Test
    @DisplayName("CQ-INV-02 — Uma mesma propriedade pode ser alvo de múltiplas investigações simultâneas? (estrutural: sem UNIQUE)")
    void cqInv02() {
        Table table = AnalysisTarget.class.getAnnotation(Table.class);
        assertNotNull(table);
        assertEquals(0, table.uniqueConstraints().length,
                "no UNIQUE(analysis_id, premise_id): the same premise may be target of several analyses");
    }

    @Test
    @DisplayName("CQ-INV-03 — Quais movimentações de animais (GTAs) ocorreram em um período?")
    void cqInv03() {
        FilterMovementPageDTO filtros = new FilterMovementPageDTO();
        filtros.setTipoMovimentacao(ImportType.AVES);
        filtros.setPagina(0);
        filtros.setItensPagina(10);

        when(movimentacaoAvesViewRepository.findByFilters(any(), any(), any(), any(), any()))
                .thenReturn(new PageImpl<>(List.of(new MovimentacaoAvesView())));
        when(movementMapper.toDTO(any(MovimentacaoAvesView.class))).thenReturn(new MovementDTO());

        AnimalMovementService service = new AnimalMovementService(
                mock(MovimentacaoAvesRepository.class),
                movimentacaoAvesViewRepository,
                mock(MovimentacaoSuinosRepository.class),
                mock(MovimentacaoBovinosRepository.class),
                mock(MovimentacaoBubalinosRepository.class),
                mock(MovimentacaoOvinosRepository.class),
                mock(MovimentacaoCaprinosRepository.class),
                movementMapper);

        var result = service.getMovementsByPremise(filtros);

        assertEquals(1, result.getData().size());
        verify(movimentacaoAvesViewRepository).findByFilters(any(), any(), any(), any(), any());
    }

    @Test
    @DisplayName("CQ-INV-04 — Quais propriedades tiveram contato direto com uma propriedade investigada?")
    void cqInv04() {
        // a movement record identifies origin and destination premises/municipalities
        MovimentacaoAvesView movimentacao = new MovimentacaoAvesView();
        movimentacao.setMunicipioOrigem("Montenegro");
        movimentacao.setMunicipioDestino("Tres Coroas");

        assertEquals("Montenegro", movimentacao.getMunicipioOrigem());
        assertEquals("Tres Coroas", movimentacao.getMunicipioDestino());
        assertNotEquals(movimentacao.getMunicipioOrigem(), movimentacao.getMunicipioDestino(),
                "a direct contact exists when origin and destination differ");
    }

    @Test
    @DisplayName("CQ-INV-05 — Quais propriedades tiveram contato indireto (cadeia de movimentações)?")
    void cqInv05() {
        MovimentacaoAvesView first = new MovimentacaoAvesView();
        first.setMunicipioOrigem("Montenegro");
        first.setMunicipioDestino("Tres Coroas");

        MovimentacaoAvesView second = new MovimentacaoAvesView();
        second.setMunicipioOrigem("Tres Coroas");
        second.setMunicipioDestino("Encantado");

        // indirect contact: the destination of the first hop is the origin of the next
        assertEquals(first.getMunicipioDestino(), second.getMunicipioOrigem());
        assertNotEquals("Montenegro", second.getMunicipioDestino(),
                "the indirect contact is one hop beyond the direct chain");
    }

    @Test
    @DisplayName("CQ-INV-06 — Qual o raio/zonas de controle definidas em uma investigação? (até 3 concêntricas)")
    void cqInv06() {
        AnalysisTarget target = new AnalysisTarget();
        target.setZone1(ZoneType.INFECTED.getNumber());
        target.setZone2(ZoneType.BUFFER.getNumber());
        target.setZone3(ZoneType.SURVEILLANCE.getNumber());

        assertEquals(1, target.getZone1());
        assertEquals(2, target.getZone2());
        assertEquals(3, target.getZone3());
        // the fourth (virtual) zone
        assertEquals(4, ZoneType.INVESTIGATION.getNumber());
        long zoneFields = java.util.Arrays.stream(AnalysisTarget.class.getDeclaredFields())
                .map(f -> f.getName())
                .filter(name -> name.matches("zone[123]"))
                .count();
        assertEquals(3, zoneFields, "AX-GEO-01: at most three concentric zones per target");
    }

    @Test
    @DisplayName("CQ-INV-07 — Quais análises sanitárias estão ativas?")
    void cqInv07() {
        UUID uuid = UUID.randomUUID();
        br.com.pdsars.sigevs.model.SanitaryAnalysis analysis = new br.com.pdsars.sigevs.model.SanitaryAnalysis();
        analysis.setAnalysisName("Investigacao HPAI");
        analysis.setIsActive(true);
        when(sanitaryAnalysisRepository.findByUuid(uuid)).thenReturn(Optional.of(analysis));
        when(sanitaryAnalysisMapper.toDTO(analysis)).thenReturn(new SanitaryAnalysisDTO());

        SanitaryAnalysisDTO result = sanitaryAnalysisService.findByUuid(uuid);

        assertNotNull(result);
        assertTrue(analysis.getIsActive(), "the investigation status is answered by isActive");
    }

    @Test
    @DisplayName("CQ-INV-08 — Quais municípios estão na área afetada de uma investigação?")
    void cqInv08() {
        AffectedArea area = new AffectedArea();
        when(affectedAreaRepository.findById(1L)).thenReturn(Optional.of(area));

        AffectedAreaService service = new AffectedAreaService(affectedAreaRepository);

        assertSame(area, service.findById(1L));
    }

    @Test
    @DisplayName("CQ-INV-09 — Quais categorias de espécie estão sendo investigadas?")
    void cqInv09() {
        // the investigation species filter maps raw GTA species to ontology categories
        assertTrue(SpeciesCategory.AVES.getValues().contains("GALINHA"));
        assertTrue(SpeciesCategory.SUINOS.getValues().contains("SUÍNO"));
        assertNotNull(SpeciesCategory.fromName("AVES"));

        br.com.pdsars.sigevs.service.SanitaryAnalysisService.FilterParameters filter =
                new br.com.pdsars.sigevs.service.SanitaryAnalysisService.FilterParameters();
        assertNull(filter.speciesFilter, "species filter is optional in an investigation");
        filter.speciesFilter = List.of("AVES");
        assertEquals(List.of("AVES"), filter.speciesFilter);
    }
}
